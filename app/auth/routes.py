from fastapi import APIRouter, HTTPException, Depends
from app.utils.database import get_db
from app.utils.otp import send_otp
from .models import User
from .schemas import Email, UserInfo
from app.utils import redis_client

router = APIRouter()


@router.post("/enter-mail")
async def enter_email(Mail: Email, db=Depends(get_db)):
    user = db.users.find_one({"email": Mail.email})
    if user:
        send_otp(email=user.get("email"))
        return {"message": "User found, OTP sent", "is_new_user": False}
    else:
        new_user = User(email=Mail.email)
        db.users.insert_one(new_user.model_dump())
        send_otp(email=Mail.email)
        return {"message": "User created, OTP sent", "is_new_user": True}


@router.post("/verify-otp")
async def verify_otp(mail: Email, otp: int, is_new_user: bool, db=Depends(get_db)):
    user = db.users.find_one({"email": mail.email})
    otp_from_redis = redis_client.get_otp(mail.email)
    if otp_from_redis:
        otp_from_redis = otp_from_redis.decode('utf-8')  
    print(f"OTP {otp} and otp from redis {otp_from_redis}")
    if user and otp_from_redis == str(otp):
        redis_client.delete_otp(mail.email)
        if is_new_user:
            return {"message": "OTP verified", "user": None}
        else:
            return {"message": "OTP verified", "user": user}
    else:
        raise HTTPException(status_code=400, detail="Invalid OTP")


@router.post("/resend-otp")
async def resend_otp(mail: Email, db=Depends(get_db)):
    user = db.users.find_one({"email": mail.email})
    if user:
        send_otp(email=user.get("email"))
        return {"message": "OTP resent"}
    else:
        raise HTTPException(status_code=404, detail="User not found")


@router.post("/register")
async def register_user(user_info: UserInfo, mail: Email, db=Depends(get_db)):
    db.users.update_one({"email": mail.email}, {"$set": user_info.model_dump()})
    return {"message": "User information updated"}


@router.put("/modify_user")
async def modify_user(user_info: UserInfo, mail: Email, db=Depends(get_db)):
    db.users.update_one({"email": mail.email}, {"$set": user_info.model_dump()})
    return {"message": "User information modified"}
