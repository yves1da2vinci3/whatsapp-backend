from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from app.database import Base
from app.enums import ChatType, MessageType
import app.association_tables as association_tables
import datetime


class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    image = Column(String)
    created_time = Column(DateTime, default=datetime.datetime.now())
    type = Column(Enum(ChatType), nullable=False)
    admin_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    admin = relationship("User", back_populates="chats")
    participants = relationship(
        "User", secondary=association_tables.user_chats, back_populates="chats"
    )
    messages = relationship("Message", back_populates="chat")


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    type = Column(Enum(MessageType), nullable=False)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    chat = relationship("Chat", back_populates="messages")
    user = relationship("User", back_populates="messages")
