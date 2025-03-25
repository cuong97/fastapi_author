from pydantic import BaseModel, validator
from typing import Optional, List


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str
    role: str

    @validator('email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email format')
        return v

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v


class UserResponse(UserBase):
    id: int
    role: str

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
