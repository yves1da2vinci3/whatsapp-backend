from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from .models import Call
from .schemas import CallCreate, CallUpdate
from .repository import CallRepository
router = APIRouter()

@router.post("/create")
async def create_call(call: CallCreate, db: Session = Depends(get_db)):
    call_repo = CallRepository(db)
    new_call = Call(**call.dict())
    created_call = call_repo.create_call(new_call)
    return created_call

@router.get("/{call_id}")
async def get_call(call_id: int, db: Session = Depends(get_db)):
    call_repo = CallRepository(db)
    call = call_repo.get_call_by_id(call_id)
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")
    return call

@router.put("/{call_id}")
async def update_call(call_id: int, call: CallUpdate, db: Session = Depends(get_db)):
    call_repo = CallRepository(db)
    result = call_repo.update_call(call_id, call.dict())
    if not result:
        raise HTTPException(status_code=404, detail="Call not found")
    return call_repo.get_call_by_id(call_id)

@router.get("/")
async def get_all_calls(db: Session = Depends(get_db)):
    call_repo = CallRepository(db)
    return call_repo.get_all_calls()
