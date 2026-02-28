from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.modules.accounts.schemas import AccountCreate
from app.modules.accounts.service import create_account, get_all_accounts
from app.db.session import SessionLocal

# Router groups endpoints
router = APIRouter()

def get_db():
    db = SessionLocal()

    try:
        yield db 
    
    finally:
        db.close() 



@router.get("/accounts")
def get_accounts(db: Session = Depends(get_db)):

    accounts = get_all_accounts(db)

    # Convert db objects into safe response format
    return [
        {
            "name": account.name
        }
        for account in accounts
    ]



# POST endpoint to create a new account
@router.post("/accounts")
def create_account_endpoint(
    account: AccountCreate, 
    db: Session = Depends(get_db)):

    # Call service layer
    new_account = create_account(
        db,
        account.user_id,
        account.name,
        account.account_type,
        account.balance
    )

    # Return safe response
    return {
        "name": new_account.name
    } 
