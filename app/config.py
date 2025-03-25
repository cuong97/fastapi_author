import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://fastapi_user:fastapi_password@localhost/fastapi_auth_db")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "supersecretkey")  # Đổi thành key bảo mật
    ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 phút
    REFRESH_TOKEN_EXPIRE_DAYS = 7  # 7 ngày


settings = Settings()
