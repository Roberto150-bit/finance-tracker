from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.modules.accounts.schemas import AccountCreate
from app.modules.accounts.service import create_account, get_all_accounts, calculate_balance
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
            "id": account.id.hex(), # hex() converts binary UUID into readable string
            "user_id": account.user_id.hex(),
            "name": account.name,
            "account_type": account.account_type,
            "balance": calculate_balance(db, account.id)
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

@router.get("/accounts/{account_id}/balance")
def get_account_balance(
    account_id: str,
    db: Session = Depends(get_db)):

    # Convert hex str -> bytes
    account_bytes = bytes.fromhex(account_id)

    balance = calculate_balance(
        db,
        account_bytes
    )

    return {
        "balance": balance
    }