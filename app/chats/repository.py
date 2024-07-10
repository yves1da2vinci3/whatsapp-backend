from sqlalchemy.orm import Session
from .models import Chat
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

    def update_chat(self, chat_id: int, chat_info: dict) -> int:
        result = self.db.query(Chat).filter(Chat.id == chat_id).update(chat_info)
        self.db.commit()
        return result

    def get_all_chats(self) -> List[Chat]:
        return self.db.query(Chat).all()
