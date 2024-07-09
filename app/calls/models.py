from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
import datetime

class Call(Base):
    __tablename__ = "calls"
    id = Column(Integer, primary_key=True)
    caller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    duration = Column(Integer, nullable=False)  # Duration in seconds
    called_at = Column(DateTime, default=datetime.datetime.now)

    caller = relationship("User", foreign_keys=[caller_id], back_populates="calls_made")
    receiver = relationship(
        "User", foreign_keys=[receiver_id], back_populates="calls_received"
    )
