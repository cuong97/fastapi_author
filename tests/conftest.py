import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Role, User
from app.config import settings

# Test database URL
TEST_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/test_db"

@pytest.fixture(scope="session")
def test_engine():
    """Create test database engine"""
    engine = create_engine(TEST_DATABASE_URL)
    return engine

@pytest.fixture(scope="session", autouse=True)
def setup_database(test_engine):
    """Create all tables in test database"""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def db_session(test_engine, setup_database):
    """Create a fresh database session for each test"""
    connection = test_engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()
    # Create default roles if they don't exist
    default_roles = ["Admin", "User", "Moderator"]
    for role_name in default_roles:
        role = session.query(Role).filter(Role.name == role_name).first()
        if not role:
            role = Role(name=role_name)
            session.add(role)
    
    session.commit()
    
    yield session
    
    # Rollback transaction after test
    session.close()
    transaction.rollback()
    connection.close()

