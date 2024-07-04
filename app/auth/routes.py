from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer
from app.utils.database import get_db
from app.utils.otp import send_otp
from .models import User
from .schemas import Email, UserInfo, TokenResponse, RefreshTokenRequest
from app.utils import redis_client
from app.utils.token import token_manager

router = APIRouter()
oauth2_scheme = HTTPBearer()


def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = token.credentials
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_data = token_manager.validate_token(payload)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_data


@router.post("/enter-mail")
async def enter_email(mail: Email, db=Depends(get_db)):
    user = db.users.find_one({"email": mail.email})
    if user:
        send_otp(email=user["email"])
        return {"message": "User found, OTP sent", "is_new_user": False}
    else:
        new_user = User(email=mail.email)
        db.users.insert_one(new_user.model_dump())
        send_otp(email=mail.email)
        return {"message": "User created, OTP sent", "is_new_user": True}


@router.post("/verify-otp", response_model=TokenResponse)
async def verify_otp(mail: Email, otp: int, is_new_user: bool, db=Depends(get_db)):
    user = db.users.find_one({"email": mail.email})
    otp_from_redis = redis_client.get_otp(mail.email)
    if otp_from_redis:
        otp_from_redis = otp_from_redis.decode("utf-8")

    if user and otp_from_redis == str(otp):
        redis_client.delete_otp(mail.email)
        access_token = token_manager.create_access_token({"email": mail.email})
        refresh_token = token_manager.create_refresh_token(mail.email)
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            is_new_user=is_new_user,
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP"
        )


@router.post("/resend-otp")
async def resend_otp(mail: Email, db=Depends(get_db)):
    user = db.users.find_one({"email": mail.email})
    if user:
        send_otp(email=user["email"])
        return {"message": "OTP resent"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


@router.post("/register")
async def register_user(
    user_info: UserInfo,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_db),
):
    result = db.users.update_one(
        {"email": current_user["email"]}, {"$set": user_info.model_dump()}
    )
    if result.modified_count:
        return {"message": "User information updated"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


@router.put("/modify_user")
async def modify_user(
    user_info: UserInfo,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_db),
):
    result = db.users.update_one(
        {"email": current_user["email"]}, {"$set": user_info.model_dump()}
    )
    if result.modified_count:
        return {"message": "User information modified"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


@router.post("/refresh-token", response_model=TokenResponse)
async def refresh_token(refresh_tokenRequest: RefreshTokenRequest):
    new_tokens = token_manager.refresh_tokens(refresh_tokenRequest.refresh_token)
    if new_tokens:
        return TokenResponse(
            access_token=new_tokens["access_token"],
            refresh_token=new_tokens["refresh_token"],
            token_type="bearer",
            is_new_user=False,
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )


@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    token_manager.revoke_refresh_token(current_user["email"])
    return {"message": "Successfully logged out"}
