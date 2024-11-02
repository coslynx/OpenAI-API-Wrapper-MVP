from fastapi import HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import jwt 
from datetime import datetime, timedelta
from .config import config  # for environment settings
from .models import UserModel  # for user model
from .schemas import TokenPayload # for JWT payload schema

JWT_SECRET_KEY = config.get_jwt_secret_key()
JWT_ALGORITHM = "HS256"

def generate_jwt(user: UserModel, expires_delta: timedelta = None) -> str:
    """Generates a JWT token for the given user.

    Args:
        user (UserModel): The user object for whom the token is generated.
        expires_delta (timedelta, optional): The time delta for token expiration. Defaults to None (using default expiration).

    Returns:
        str: The generated JWT token.
    """
    to_encode = {"sub": user.id, "exp": datetime.utcnow() + (expires_delta or timedelta(minutes=15))}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def validate_jwt(token: str) -> Dict[str, Any]:
    """Validates a JWT token.

    Args:
        token (str): The JWT token to be validated.

    Returns:
        Dict[str, Any]: The decoded JWT payload if the token is valid.
        Raises:
            HTTPException: If the token is invalid or expired.

    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        # Check if the token has expired
        if datetime.fromtimestamp(payload["exp"]) < datetime.utcnow():
            raise HTTPException(status_code=401, detail="Token expired")
        return payload
    except jwt.exceptions.InvalidSignatureError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=401, detail="Invalid token")