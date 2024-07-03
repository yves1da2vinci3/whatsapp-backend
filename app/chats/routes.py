from fastapi import APIRouter, HTTPException, Depends
from app.utils.database import get_db
from .models import Chat, Message
from .schemas import MessageCreate

router = APIRouter()

@router.get("/")
async def get_all_chats(user_id: str, db=Depends(get_db)):
    chats = list(db.chats.find({"participants": user_id}))
    return chats

@router.get("/{chat_id}")
async def get_chat(chat_id: str, db=Depends(get_db)):
    chat = db.chats.find_one({"_id": chat_id})
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat

@router.post("/{chat_id}/send_message")
async def send_message(chat_id: str, message: MessageCreate, db=Depends(get_db)):
    db.chats.update_one({"_id": chat_id}, {"$push": {"messages": message.dict()}})
    return {"message": "Message sent"}

@router.delete("/{chat_id}/delete_message")
async def delete_message(chat_id: str, message_id: str, db=Depends(get_db)):
    db.chats.update_one({"_id": chat_id}, {"$pull": {"messages": {"_id": message_id}}})
    return {"message": "Message deleted"}

@router.get("/{chat_id}/media")
async def get_media(chat_id: str, db=Depends(get_db)):
    chat = db.chats.find_one({"_id": chat_id})
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    media = [msg for msg in chat['messages'] if msg['type'] in ['video', 'audio', 'image', 'file']]
    return media
