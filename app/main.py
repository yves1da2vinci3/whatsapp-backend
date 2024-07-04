from fastapi import FastAPI
from app.auth.routes import router as auth_router
from app.chats.routes import router as chats_router
from app.stories.routes import router as stories_router
from app.calls.routes import router as calls_router
from app.upload.routes import router as upload_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(chats_router, prefix="/chats", tags=["chats"])
app.include_router(stories_router, prefix="/stories", tags=["stories"])
app.include_router(calls_router, prefix="/calls", tags=["calls"])
app.include_router(upload_router, prefix="/upload", tags=["upload"])


@app.get("/")
async def root():
    return {"message": "Welcome to the whataspp API"}