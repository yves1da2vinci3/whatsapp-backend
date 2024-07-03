from fastapi import APIRouter, HTTPException, Depends
from app.utils.database import get_db
from .models import Call
from .models import CallCreate

router = APIRouter()

@router.post("/make_call")
async def make_call(call: CallCreate, db=Depends(get_db)):
    db.calls.insert_one(call.dict())
    return {"message": "Call initiated"}

@router.get("/history")
async def get_call_history(user_id: str, db=Depends(get_db)):
    calls = list(db.calls.find({"participants": user_id}))
    return calls

@router.get("/history/{call_id}")
async def get_one_call_history(call_id: str, db=Depends(get_db)):
    call = db.calls.find_one({"_id": call_id})
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")
    return call
