# Route - receives html requests

# APIRouter lets us group endpoints togeter
from fastapi import APIRouter, Depends

# Session is the db connection type
from sqlalchemy.orm import Session

# Schema = structure of incoming request data
from app.modules.users.schemas import UserCreate

# Service = business logic 
from app.modules.users.service import create_user, get_all_users

# SessionLocal creates db sessions
from app.db.session import SessionLocal



# Router groups endpoints
router = APIRouter()

# This function creates a db session
# Every request gets its own session
def get_db():
    db = SessionLocal()

    try:
        yield db    # returns the db session to FastAPI
    
    finally:
        db.close()  # always close the connection


# Simple test endpoint
@router.get("/users")
def get_users(db: Session = Depends(get_db)):

    users = get_all_users(db)

    # Convert db objects into safe response format
    return [
        {
            "email": user.email
        }
        for user in users
    ]



# POST endpoint to create a new user
@router.post("/users")
def create_user_endpoint(
    user: UserCreate,               # FastAPI automatically reads JSON and validates it
    db: Session = Depends(get_db)):   # FastAPI automatically injects db session

    # Call service layer
    new_user = create_user(
        db,
        user.email,
        user.password
    )

    # Return safe response
    return {
        "email": new_user.email
    }