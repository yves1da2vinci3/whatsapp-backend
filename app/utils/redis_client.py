import redis
from typing import Dict, Any

redis_client = redis.StrictRedis(host="localhost", port=6379, db=0)

# Define namespace prefixes
OTP_PREFIX = "otp:"
SESSION_PREFIX = "session:"
STORIES_PREFIX = "stories:"


# OTP functions
def set_otp(user_id: str, otp: str, expiry: int = 300) -> bool:
    """Set OTP for a user with expiry (default 5 minutes)"""
    key = f"{OTP_PREFIX}{user_id}"
    return redis_client.setex(key, expiry, otp)


def get_otp(user_id: str) -> str:
    """Get OTP for a user"""
    key = f"{OTP_PREFIX}{user_id}"
    return redis_client.get(key)


def delete_otp(user_id: str) -> int:
    """Delete OTP for a user"""
    key = f"{OTP_PREFIX}{user_id}"
    return redis_client.delete(key)


# Session functions
def set_session(session_id: str, data: Dict[str, Any]) -> bool:
    """Set session data"""
    key = f"{SESSION_PREFIX}{session_id}"
    return redis_client.hmset(key, data)


def get_session(session_id: str) -> Dict[str, Any]:
    """Get session data"""
    key = f"{SESSION_PREFIX}{session_id}"
    return redis_client.hgetall(key)


def delete_session(session_id: str) -> int:
    """Delete session data"""
    key = f"{SESSION_PREFIX}{session_id}"
    return redis_client.delete(key)


# Stories functions
def set_story(story_id: str, data: Dict[str, Any]) -> bool:
    """Set story data"""
    key = f"{STORIES_PREFIX}{story_id}"
    return redis_client.hmset(key, data)


def get_story(story_id: str) -> Dict[str, Any]:
    """Get story data"""
    key = f"{STORIES_PREFIX}{story_id}"
    return redis_client.hgetall(key)


def delete_story(story_id: str) -> int:
    """Delete story data"""
    key = f"{STORIES_PREFIX}{story_id}"
    return redis_client.delete(key)
