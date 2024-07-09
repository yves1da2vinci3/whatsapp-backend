from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database import Base

user_chats = Table('user_chats', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('chat_id', Integer, ForeignKey('chats.id'))
)
