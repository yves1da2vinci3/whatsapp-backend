from fastapi import APIRouter, HTTPException, Depends
from app.utils.database import get_db
from .models import Story
from .schemas import StoryCreate

router = APIRouter()

@router.post("/")
async def create_story(story: StoryCreate, db=Depends(get_db)):
    db.stories.insert_one(story.dict())
    return {"message": "Story created"}

@router.get("/")
async def get_stories(user_id: str, db=Depends(get_db)):
    stories = list(db.stories.find({"user_id": user_id}))
    return stories
