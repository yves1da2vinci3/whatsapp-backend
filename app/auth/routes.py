from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.otp import send_otp
from .models import User
from .schemas import (
    Email,
    UserInfo,
    TokenResponse,
    RefreshTokenRequest,
    ModifyUserRequest,
)
from app.utils import redis_client
from app.utils.token import token_manager
from .repository import UserRepository

router = APIRouter()
security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    print("Received token:", credentials.credentials)
    user_data = token_manager.validate_token(credentials.credentials)
    print("Validated user data:", user_data)
    if not user_data:
        print("Raising 401 exception")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_data


@router.post("/enter-mail")
async def enter_email(mail: Email, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    user = user_repo.get_user_by_email(mail.email)
    if user:
        send_otp(email=user.email)
        return {"message": "User found, OTP sent", "is_new_user": False}
    else:
        new_user = User(email=mail.email)
        user_repo.create_user(new_user)
        send_otp(email=mail.email)
        return {"message": "User created, OTP sent", "is_new_user": True}


@router.post("/verify-otp", response_model=TokenResponse)
async def verify_otp(mail: Email, otp: int, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    user = user_repo.get_user_by_email(mail.email)
    user_id = user.to_dict().get("id")
    print(f"user: ${user.to_dict()}")
    otp_from_redis = redis_client.get_otp(mail.email)
    if otp_from_redis:
        otp_from_redis = otp_from_redis.decode("utf-8")

    if user and otp_from_redis == str(otp):
        redis_client.delete_otp(mail.email)
        access_token = token_manager.create_access_token(
            {"email": mail.email, "id": user_id}
        )
        refresh_token = token_manager.create_refresh_token(mail.email, user_id)
        userToSend = None
        userToSend = UserInfo(**user.to_dict())

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            user=userToSend.model_dump(),
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP"
        )


@router.post("/resend-otp")
async def resend_otp(mail: Email, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    user = user_repo.get_user_by_email(mail.email)
    if user:
        send_otp(email=user.email)
        return {"message": "OTP resent"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


@router.post("/register")
async def register_user(
    user_info: ModifyUserRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_repo = UserRepository(db)

    result = user_repo.update_user(current_user["email"], user_info.model_dump())
    if result:
        return {"message": "User information updated"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


@router.put("/modify_user")
async def modify_user(
    user_info: ModifyUserRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_repo = UserRepository(db)
    result = user_repo.update_user(current_user["email"], user_info.model_dump())
    user = user_repo.get_user_by_email(current_user["email"])
    if result:
        return {"message": "User information modified", "user": user.to_dict()}
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
            refresh_token="",
            token_type="bearer",
            user={},  # Assuming no user information needed here
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


@router.get("/users")
async def get_users(
    db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)
):
    user_repo = UserRepository(db)
    users = user_repo.get_all_users(current_user["email"])
    return {"users": users}
