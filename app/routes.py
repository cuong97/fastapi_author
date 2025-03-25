import logging
from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Role
from app.rbac.dependencies import get_current_user
from app.schemas import UserCreate, UserResponse, TokenData
from app.utils import (
    hash_password, verify_password, create_access_token,
)
from datetime import timedelta
from app.config import settings

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)) -> dict[str, Any]:
    """
    Register a new user.
    
    Args:
        user: User creation data
        db: Database session
        
    Returns:
        Dict[str, Any]: Created user data
        
    Raises:
        HTTPException: If username exists or role is invalid
    """
    try:
        logger.info(f"Attempting to register user: {user.username}")

        # Check if username exists
        db_user = db.query(User).filter(User.username == user.username).first()
        if db_user:
            logger.warning(f"Username already exists: {user.username}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )

        # Get role
        role: Optional[Role] = db.query(Role).filter(Role.name == user.role).first()
        if not role:
            logger.warning(f"Invalid role requested: {user.role}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid role"
            )

        # Create new user
        new_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hash_password(user.password),
            role_id=role.id
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        logger.info(f"Successfully registered user: {user.username}")

        return {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "role": role.name
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error registering user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error registering user"
        )


@router.post("/login", response_model=TokenData)
def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
) -> dict[str, Any]:
    """
    Login user and return JWT tokens.
    
    Args:
        form_data: Login form data
        db: Database session
        
    Returns:
        Dict[str, Any]: Access and refresh tokens
        
    Raises:
        HTTPException: If credentials are invalid
    """
    try:
        logger.info(f"Login attempt for user: {form_data.username}")

        user = db.query(User).filter(User.username == form_data.username).first()
        if not user or not verify_password(form_data.password, user.hashed_password):
            logger.warning(f"Invalid credentials for user: {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create tokens
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )

        refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        refresh_token = create_access_token(
            data={"sub": user.username}, expires_delta=refresh_token_expires
        )

        logger.info(f"Successfully logged in user: {form_data.username}")

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error during login"
        )


@router.get("/me", response_model=UserResponse)
def read_users_me(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
) -> dict[str, Any]:
    """
    Get current user information.
    
    Args:
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Dict[str, Any]: Current user information
        
    Raises:
        HTTPException: If user role not found
    """
    try:
        logger.info(f"Fetching user information for: {current_user.username}")

        # Get role name
        role: Optional[Role] = db.query(Role).filter(Role.id == current_user.role_id).first()
        if not role:
            logger.error(f"Role not found for user: {current_user.username}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="User role not found"
            )

        logger.info(f"Successfully fetched user information for: {current_user.username}")

        return {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "role": role.name
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching user information: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching user information"
        )
