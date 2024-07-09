from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base
import app.association_tables as association_tables

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    image = Column(String)
    contacts = Column(Text)  # Storing list of contacts as a string (could be JSON if preferred)

    chats = relationship('Chat', secondary=association_tables.user_chats, back_populates='participants')
    messages = relationship('Message', back_populates='user')
    stories = relationship('Story', back_populates='user')
    calls_made = relationship('Call', foreign_keys='Call.caller_id', back_populates='caller')
    calls_received = relationship('Call', foreign_keys='Call.receiver_id', back_populates='receiver')
