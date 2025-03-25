import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta, UTC
from passlib.context import CryptContext

from jose import jwt
from app.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthError(Exception):
    """Base exception for authentication errors"""
    pass


class InvalidCredentialsError(AuthError):
    """Raised when credentials are invalid"""
    pass


class TokenError(AuthError):
    """Raised when there's an error with JWT tokens"""
    pass


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Args:
        password: The plain text password to hash
        
    Returns:
        str: The hashed password
    """
    try:
        return pwd_context.hash(password)
    except Exception as e:
        logger.error(f"Error hashing password: {str(e)}")
        raise AuthError("Error hashing password")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    
    Args:
        plain_password: The plain text password to verify
        hashed_password: The hashed password to verify against
        
    Returns:
        bool: True if password matches, False otherwise
    """
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        logger.error(f"Error verifying password: {str(e)}")
        raise AuthError("Error verifying password")


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: The data to encode in the token
        expires_delta: Optional expiration time delta
        
    Returns:
        str: The encoded JWT token
        
    Raises:
        TokenError: If there's an error creating the token
    """
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(UTC) + expires_delta
        else:
            expire = datetime.now(UTC) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm="HS256")
        return encoded_jwt
    except Exception as e:
        logger.error(f"Error creating access token: {str(e)}")
        raise TokenError("Error creating access token")


def verify_token(token: str) -> Dict[str, Any]:
    """
    Verify a JWT token.
    
    Args:
        token: The JWT token to verify
        
    Returns:
        Dict[str, Any]: The decoded token payload
        
    Raises:
        TokenError: If the token is invalid or expired
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        logger.error("Token has expired")
        raise TokenError("Token has expired")
    except jwt.JWTError as e:
        logger.error(f"Invalid token: {str(e)}")
        raise TokenError("Invalid token")
    except Exception as e:
        logger.error(f"Error verifying token: {str(e)}")
        raise TokenError("Error verifying token")

def check_password_strength(password: str) -> bool:
    """
    Check if password meets minimum strength requirements.

    Requirements:
    - At least 8 characters long
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one number
    - Contains at least one special character

    Args:
        password: Password string to validate

    Returns:
        bool: True if password meets requirements, False otherwise
    """
    if len(password) < 8:
        return False

    has_upper = False
    has_lower = False
    has_digit = False
    has_special = False

    for char in password:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True
        elif not char.isalnum():
            has_special = True

    return has_upper and has_lower and has_digit and has_special
