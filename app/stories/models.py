from sqlalchemy import Column, Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.enums import StoryType

class Story(Base):
    __tablename__ = 'stories'
    id = Column(Integer, primary_key=True)
    type = Column(Enum(StoryType), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='stories')
