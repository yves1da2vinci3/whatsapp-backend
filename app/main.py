from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from app.auth.routes import router as auth_router
from app.chats.routes import router as chat_router
from app.stories.routes import router as story_router
from app.calls.routes import router as call_router
from app.upload.routes import router as upload_router
# from app.database import Base, engine


# # Create tables
# Base.metadata.create_all(bind=engine)


def init_middleware(app):
    Instrumentator().instrument(app).expose(app)


app = FastAPI()

init_middleware(app)

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(chat_router, prefix="/api/chats", tags=["chats"])
app.include_router(story_router, prefix="/api/stories", tags=["stories"])
app.include_router(call_router, prefix="/api/calls", tags=["calls"])
app.include_router(upload_router, prefix="/api/upload", tags=["upload"])


@app.get("/", tags=["root"])
async def root():
    """
    Welcome message
    """
    return {"message": "Welcome to the whatsapp API"}
