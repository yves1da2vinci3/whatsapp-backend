from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from .models import Chat
from  .schemas import ChatCreate, ChatUpdate
from .repository import ChatRepository
router = APIRouter()

@router.post("/create")
async def create_chat(chat: ChatCreate, db: Session = Depends(get_db)):
    chat_repo = ChatRepository(db)
    new_chat = Chat(**chat.mode_dump())
    created_chat = chat_repo.create_chat(new_chat)
    return created_chat

@router.get("/{chat_id}")
async def get_chat(chat_id: int, db: Session = Depends(get_db)):
    chat_repo = ChatRepository(db)
    chat = chat_repo.get_chat_by_id(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat

@router.put("/{chat_id}")
async def update_chat(chat_id: int, chat: ChatUpdate, db: Session = Depends(get_db)):
    chat_repo = ChatRepository(db)
    result = chat_repo.update_chat(chat_id, chat.mode_dump())
    if not result:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat_repo.get_chat_by_id(chat_id)

@router.get("/")
async def get_all_chats(db: Session = Depends(get_db)):
    chat_repo = ChatRepository(db)
    return chat_repo.get_all_chats()
