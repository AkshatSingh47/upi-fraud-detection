from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

# Password hashing with updated config
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12
)

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

def hash_password(password: str) -> str:
    """Hash a password"""
    # Ensure password is not too long for bcrypt
    password = password[:72]
    try:
        return pwd_context.hash(password)
    except Exception as e:
        # Fallback: if still failing, use first 50 characters
        return pwd_context.hash(password[:50])

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against hash"""
    # Ensure password is not too long for bcrypt
    plain_password = plain_password[:72]
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        # Fallback: try with first 50 characters
        return pwd_context.verify(plain_password[:50], hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str):
    """Decode JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.JWTError:
        return None

