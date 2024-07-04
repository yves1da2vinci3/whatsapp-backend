from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.utils.database import get_db
from app.utils.otp import send_otp
from .models import User
from .schemas import Email, UserInfo

router = APIRouter()


@router.post("/enter_mail")
async def enter_email(Mail: Email, db=Depends(get_db)):
    user = db.users.find_one({"email": Mail.email})
    if user:
        return user
    else:
        new_user = User(email=Mail.email)
        db.users.insert_one(new_user.model_dump())
        send_otp(email=Mail.email)
        return {"message": "User created, OTP sent"}


@router.post("/register_user")
async def register_user(user_info: UserInfo, mail: Email, db=Depends(get_db)):
    db.users.update_one({"email": mail.email}, {"$set": user_info.model_dump()})
    return {"message": "User information updated"}


@router.put("/modify_user")
async def modify_user(user_info: UserInfo, mail: Email, db=Depends(get_db)):
    db.users.update_one({"email": mail.email}, {"$set": user_info.model_dump()})
    return {"message": "User information modified"}
