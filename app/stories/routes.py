from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from .models import Story
from .schemas import StoryCreate, StoryUpdate
from .repository import StoryRepository
from typing import List
router = APIRouter()

@router.post("/create", response_model=Story)
async def create_story(story: StoryCreate, db: Session = Depends(get_db)):
    story_repo = StoryRepository(db)
    new_story = Story(**story.dict())
    created_story = story_repo.create_story(new_story)
    return created_story

@router.get("/{story_id}", response_model=Story)
async def get_story(story_id: int, db: Session = Depends(get_db)):
    story_repo = StoryRepository(db)
    story = story_repo.get_story_by_id(story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return story

@router.put("/{story_id}", response_model=Story)
async def update_story(story_id: int, story: StoryUpdate, db: Session = Depends(get_db)):
    story_repo = StoryRepository(db)
    result = story_repo.update_story(story_id, story.dict())
    if not result:
        raise HTTPException(status_code=404, detail="Story not found")
    return story_repo.get_story_by_id(story_id)

@router.get("/", response_model=List[Story])
async def get_all_stories(db: Session = Depends(get_db)):
    story_repo = StoryRepository(db)
    return story_repo.get_all_stories()
