import jwt
from datetime import datetime, timedelta
from typing import Dict, Optional
from .redis_client import set_session, get_session, delete_session
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()


class TokenManager:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.access_token_expire_minutes = 30
        self.refresh_token_expire_days = 30

    def create_access_token(self, data: Dict) -> str:
        to_encode = data.copy()
        expire = datetime.now() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm="HS256")
        return encoded_jwt

    def create_refresh_token(self, email: str, id: int) -> str:
        expire = datetime.now() + timedelta(days=self.refresh_token_expire_days)
        refresh_token = jwt.encode(
            {"email": email, "id": id, "exp": expire},
            self.secret_key,
            algorithm="HS256",
        )
        set_session(
            email,
            {
                "expiresIn": int(
                    timedelta(days=self.refresh_token_expire_days).total_seconds()
                ),
                "refresh_token": refresh_token,
            },
        )
        return refresh_token

    def validate_token(self, token: str) -> Optional[Dict]:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def refresh_tokens(self, refresh_token: str) -> Optional[Dict[str, str]]:
        try:
            payload = jwt.decode(refresh_token, self.secret_key, algorithms=["HS256"])
            print(f"payload:  {payload}")
            email = payload.get("email")
            id = payload.get("id")
            stored_session = get_session(email)
            refresh_token_from_redis = stored_session[b"refresh_token"].decode("utf-8")
            print(f" refresh token stored_session:  {refresh_token_from_redis}")

            if stored_session and refresh_token_from_redis == refresh_token:
                new_access_token = self.create_access_token({"email": email, "id": id})
                return {
                    "access_token": new_access_token,
                }
            return None
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def revoke_refresh_token(self, email: str):
        delete_session(email)


# Initialize the TokenManager with the secret key from environment variables
token_manager = TokenManager(os.getenv("SECRET_KEY"))
