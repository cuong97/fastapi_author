import pytest
from datetime import timedelta
from app.utils import hash_password, verify_password, create_access_token, verify_token, TokenError, \
    check_password_strength


def test_hash_password():
    """Test password hashing"""
    password = "Test123!@#"
    hashed = hash_password(password)
    assert hashed != password
    assert isinstance(hashed, str)
    assert len(hashed) > 0


def test_verify_password():
    """Test password verification"""
    password = "Test123!@#"
    hashed = hash_password(password)
    assert verify_password(password, hashed)
    assert not verify_password("wrong_password", hashed)


def test_create_access_token():
    """Test JWT token creation"""
    data = {"sub": "testuser"}
    token = create_access_token(data)
    assert isinstance(token, str)
    assert len(token) > 0


def test_verify_token():
    """Test JWT token verification"""
    data = {"sub": "testuser"}
    token = create_access_token(data)
    decoded = verify_token(token)
    assert decoded["sub"] == "testuser"


def test_verify_expired_token():
    """Test verification of expired token"""
    data = {"sub": "testuser"}
    token = create_access_token(data, expires_delta=timedelta(seconds=-1))
    with pytest.raises(TokenError):
        verify_token(token)


def test_check_password_strength():
    """Test password strength validation"""
    # Strong password
    assert check_password_strength("Test123!@#")
    assert check_password_strength("Password123!@#")
    # Password strength validation function

    # Weak passwords
    assert not check_password_strength("weak")
    assert not check_password_strength("12345678")
    assert not check_password_strength("abcdefgh")
    assert not check_password_strength("ABCDEFGH")
    assert not check_password_strength("!@#$%^&*")
