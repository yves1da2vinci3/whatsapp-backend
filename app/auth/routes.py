from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.utils.database import get_db
from app.utils.otp import send_otp
from .models import User
from .schemas import PhoneNumber, UserInfo

router = APIRouter()

@router.post("/enter_number")
async def enter_number(phone: PhoneNumber, db=Depends(get_db)):
    user = db.users.find_one({"phone": phone.number})
    if user:
        return user
    else:
        new_user = User(phone=phone.number)
        db.users.insert_one(new_user.model_dump())
        send_otp(phone.number)
        return {"message": "User created, OTP sent"}

@router.post("/register_user")
async def register_user(user_info: UserInfo, phone: PhoneNumber, db=Depends(get_db)):
    db.users.update_one({"phone": phone.number}, {"$set": user_info.model_dump()})
    return {"message": "User information updated"}

@router.put("/modify_user")
async def modify_user(user_info: UserInfo, phone: PhoneNumber, db=Depends(get_db)):
    db.users.update_one({"phone": phone.number}, {"$set": user_info.model_dump()})
    return {"message": "User information modified"}
