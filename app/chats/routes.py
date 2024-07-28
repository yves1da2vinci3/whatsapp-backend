from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from .models import Chat, Message
from .schemas import (
    ChatCreate,
    ChatUpdate,
    ChatResponse,
    MessageCreate,
    MessageResponse,
)
from .repository import ChatRepository
from app.auth.routes import get_current_user
from app.auth.models import User

router = APIRouter()
security = HTTPBearer()


@router.post("/", response_model=ChatResponse)
async def create_chat(
    chat: ChatCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    chat_repo = ChatRepository(db)
    new_chat = Chat(**chat.model_dump(), admin_id=current_user["id"])
    created_chat = chat_repo.create_chat(new_chat)
    # create chat participants
    for participant_email in chat.participants:
        participant = db.query(User).filter(User.id == participant_email).first()
        if participant:
            chat.participants.append(participant)
    db.commit()
    db.refresh(created_chat)
    return ChatResponse.model_validate(created_chat)


@router.get("/{chat_id}", response_model=ChatResponse)
async def get_chat(
    chat_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    chat_repo = ChatRepository(db)
    chat = chat_repo.get_chat_by_id(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    if not chat_repo.is_user_in_chat(chat_id, current_user["id"]):
        raise HTTPException(
            status_code=403, detail="Not authorized to access this chat"
        )
    return ChatResponse.model_validate(chat)


@router.put("/{chat_id}", response_model=ChatResponse)
async def update_chat(
    chat_id: int,
    chat: ChatUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    chat_repo = ChatRepository(db)
    existing_chat = chat_repo.get_chat_by_id(chat_id)
    if not existing_chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    if current_user["id"] != existing_chat.admin_id:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this chat"
        )
    updated_chat = chat_repo.update_chat(chat_id, chat.model_dump(exclude_unset=True))
    return ChatResponse.model_validate(updated_chat)


@router.delete("/{chat_id}", status_code=204)
async def delete_chat(
    chat_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    chat_repo = ChatRepository(db)
    chat = chat_repo.get_chat_by_id(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    if current_user["id"] != chat.admin_id:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this chat"
        )
    chat_repo.delete_chat(chat_id)


@router.post("/{chat_id}/users/{user_id}", status_code=204)
async def add_user_to_chat(
    chat_id: int,
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    chat_repo = ChatRepository(db)
    chat = chat_repo.get_chat_by_id(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    if current_user["id"] != chat.admin_id:
        raise HTTPException(
            status_code=403, detail="Not authorized to add users to this chat"
        )
    if not chat_repo.add_user_to_chat(chat_id, user_id):
        raise HTTPException(status_code=400, detail="Failed to add user to chat")


@router.delete("/{chat_id}/users/{user_id}", status_code=204)
async def remove_user_from_chat(
    chat_id: int,
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    chat_repo = ChatRepository(db)
    chat = chat_repo.get_chat_by_id(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    if current_user["id"] != chat.admin_id:
        raise HTTPException(
            status_code=403, detail="Not authorized to remove users from this chat"
        )
    if not chat_repo.remove_user_from_chat(chat_id, user_id):
        raise HTTPException(status_code=400, detail="Failed to remove user from chat")


@router.get("/", response_model=List[ChatResponse])
async def get_user_chats(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    chat_repo = ChatRepository(db)
    chats = chat_repo.get_user_chats(current_user["id"], skip, limit)
    if not chats:
        return []
    return [
        ChatResponse(
            **chat.__dict__,
            last_message=chat.messages[0] if chat.messages else None,
        )
        for chat in chats
    ]


@router.get("/{chat_id}/messages", response_model=List[MessageResponse])
async def get_chat_messages(
    chat_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    chat_repo = ChatRepository(db)
    if not chat_repo.is_user_in_chat(chat_id, current_user["id"]):
        raise HTTPException(
            status_code=403, detail="Not authorized to access this chat"
        )
    messages = chat_repo.get_chat_messages(chat_id, skip, limit)
    return [MessageResponse.model_validate(message) for message in messages]


@router.post("/{chat_id}/messages", response_model=MessageResponse)
async def create_message(
    chat_id: int,
    message: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    chat_repo = ChatRepository(db)
    if not chat_repo.is_user_in_chat(chat_id, current_user["id"]):
        raise HTTPException(
            status_code=403, detail="Not authorized to send messages in this chat"
        )
    new_message = Message(
        **message.model_dump(), chat_id=chat_id, user_id=current_user["id"]
    )
    created_message = chat_repo.create_message(new_message)
    return MessageResponse.model_validate(created_message)


@router.delete("/{chat_id}/messages/{message_id}", status_code=204)
async def delete_message(
    chat_id: int,
    message_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    chat_repo = ChatRepository(db)
    message = chat_repo.get_message_by_id(message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    if message.chat_id != chat_id:
        raise HTTPException(
            status_code=400, detail="Message does not belong to this chat"
        )
    if message.user_id != current_user["id"]:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this message"
        )
    if not chat_repo.delete_message(message_id):
        raise HTTPException(status_code=500, detail="Failed to delete message")
