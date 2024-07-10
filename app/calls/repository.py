from sqlalchemy.orm import Session
from typing import List, Optional
from .models import Call

class CallRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_call_by_id(self, call_id: int) -> Optional[Call]:
        return self.db.query(Call).filter(Call.id == call_id).first()

    def create_call(self, call: Call) -> Call:
        self.db.add(call)
        self.db.commit()
        self.db.refresh(call)
        return call

    def update_call(self, call_id: int, call_info: dict) -> int:
        result = self.db.query(Call).filter(Call.id == call_id).update(call_info)
        self.db.commit()
        return result

    def get_all_calls(self) -> List[Call]:
        return self.db.query(Call).all()
