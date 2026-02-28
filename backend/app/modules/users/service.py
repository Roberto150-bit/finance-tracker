# DB - stores data
# Service layer talks to database
# Routes should not


# Session represents a connection to the db
from sqlalchemy.orm import Session

# Imports the User table model
from app.db.models.user import User


# This functon hanles the logic of creating a user
# Routes should NOT talk directly to the db
# Instead routes call services
def create_user(db: Session, email: str, password: str):

    # Create a new User object (this doesn't save yet)
    user = User(
        email=email,
        password=password
    )

    
    db.add(user)        # add the user to the db session
    db.commit()         # actually saves the data to the db
    db.refresh(user)    # refresh the saved data back into the objects

    return user         # returns the created user


# This function retrieves all users from the database
def get_all_users(db: Session):

    # Query means "ask the db for rows"
    users = db.query(User).all()

    return users