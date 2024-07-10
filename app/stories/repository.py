from sqlalchemy.orm import Session
from .models import Story
from typing import List, Optional

class StoryRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_story_by_id(self, story_id: int) -> Optional[Story]:
        return self.db.query(Story).filter(Story.id == story_id).first()

    def create_story(self, story: Story) -> Story:
        self.db.add(story)
        self.db.commit()
        self.db.refresh(story)
        return story

    def update_story(self, story_id: int, story_info: dict) -> int:
        result = self.db.query(Story).filter(Story.id == story_id).update(story_info)
        self.db.commit()
        return result

    def get_all_stories(self) -> List[Story]:
        return self.db.query(Story).all()
