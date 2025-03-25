from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, Role


def init_db():
    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Create a new session
    db = SessionLocal()

    try:
        # Check if roles already exist
        existing_roles = db.query(Role).all()
        if existing_roles:
            print("Roles already exist in the database")
            return

        # Create default roles
        roles = [
            Role(name="Admin"),
            Role(name="User"),
            Role(name="Moderator")
        ]

        # Add roles to database
        for role in roles:
            db.add(role)

        # Commit the changes
        db.commit()
        print("Successfully created default roles")

    except Exception as e:
        print(f"Error creating roles: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
