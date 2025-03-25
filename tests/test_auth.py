from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app

client = TestClient(app)

# Test data
test_user = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "Test123!@#",
    "role": "User"
}

test_admin = {
    "username": "admin",
    "email": "admin@example.com",
    "password": "Admin123!@#",
    "role": "Admin"
}


def test_get_current_user_invalid_token(db_session: Session):
    """Test getting current user with invalid token"""
    response = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401
