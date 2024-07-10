from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from .models import Story
from .schemas import StoryCreate
from .repository import StoryRepository
router = APIRouter()

@router.post("/create")
async def create_story(story: StoryCreate, db: Session = Depends(get_db)):
    story_repo = StoryRepository(db)
    new_story = Story(**story.dict())
    created_story = story_repo.create_story(new_story)
    return created_story

@router.get("/{story_id}")
async def get_story(story_id: int, db: Session = Depends(get_db)):
    story_repo = StoryRepository(db)
    story = story_repo.get_story_by_id(story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return story


@router.get("/")
async def get_all_stories(db: Session = Depends(get_db)):
    story_repo = StoryRepository(db)
    return story_repo.get_all_stories()
