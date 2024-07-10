from sqlalchemy import desc
from sqlalchemy.orm import Session, selectinload
from .models import Chat, Message
from app.auth.models import User
from typing import List, Optional


class ChatRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_chat_by_id(self, chat_id: int) -> Optional[Chat]:
        return self.db.query(Chat).filter(Chat.id == chat_id).first()

    def create_chat(self, chat: Chat) -> Chat:
        self.db.add(chat)
        self.db.commit()
        self.db.refresh(chat)
        return chat

    def update_chat(self, chat_id: int, chat_info: dict) -> Optional[Chat]:
        chat = self.get_chat_by_id(chat_id)
        if chat:
            for key, value in chat_info.items():
                setattr(chat, key, value)
            self.db.commit()
            self.db.refresh(chat)
        return chat

    def delete_chat(self, chat_id: int) -> bool:
        chat = self.get_chat_by_id(chat_id)
        if chat:
            self.db.delete(chat)
            self.db.commit()
            return True
        return False

    def add_user_to_chat(self, chat_id: int, user_id: int) -> bool:
        chat = self.get_chat_by_id(chat_id)
        user = self.db.query(User).get(user_id)
        if chat and user:
            chat.participants.append(user)
            self.db.commit()
            return True
        return False

    def remove_user_from_chat(self, chat_id: int, user_id: int) -> bool:
        chat = self.get_chat_by_id(chat_id)
        user = self.db.query(User).get(user_id)
        if chat and user:
            chat.participants.remove(user)
            self.db.commit()
            return True
        return False

    def is_user_in_chat(self, chat_id: int, user_id: int) -> bool:
        chat = self.get_chat_by_id(chat_id)
        if chat:
            return chat.admin_id == user_id or any(
                participant.id == user_id for participant in chat.participants
            )
        return False

    def get_user_chats(
        self, user_id: int, skip: int = 0, limit: int = 20
    ) -> List[Chat]:
        return (
            self.db.query(Chat)
            .filter((Chat.admin_id == user_id) | (Chat.participants.any(id=user_id)))
            .options(
                selectinload(
                    Chat.messages.order_by(desc(Message.created_time)).limit(1)
                )
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_chat_messages(
        self, chat_id: int, skip: int = 0, limit: int = 50
    ) -> List[Message]:
        return (
            self.db.query(Message)
            .filter(Message.chat_id == chat_id)
            .order_by(desc(Message.created_time))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_message(self, message: Message) -> Message:
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message

    def delete_message(self, message_id: int) -> bool:
        message = self.db.query(Message).get(message_id)
        if message:
            self.db.delete(message)
            self.db.commit()
            return True
        return False

    def get_message_by_id(self, message_id: int) -> Optional[Message]:
        return self.db.query(Message).get(message_id)
