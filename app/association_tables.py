from sqlalchemy import Table, Column, Integer, ForeignKey, UniqueConstraint
from app.database import Base

user_chats = Table('user_chats', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('chat_id', Integer, ForeignKey('chats.id')),
    UniqueConstraint('user_id', 'chat_id', name='uq_user_chat')
)
