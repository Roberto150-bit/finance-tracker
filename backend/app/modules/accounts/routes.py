from fastapi import (
    APIRouter, 
    Depends, 
    HTTPException)

from sqlalchemy.orm import Session

from app.modules.accounts.schemas import AccountCreate

from app.modules.accounts.service import (
    create_account, 
    get_all_accounts, 
    calculate_balance, 
    delete_account)

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

    balance = calculate_balance(db, account_bytes)

    return {
        "balance": balance
    }

@router.delete("/accounts/{account_id}")
def delete_account_endpoint(
    account_id: str,
    db: Session = Depends(get_db)):

    account_bytes = bytes.fromhex(account_id)

    try:
        delete_account(db, account_bytes)
    
    except ValueError as e:
        if "not found" in str(e):
            raise HTTPException(
                status_code=404,
                detail="Accont not found"
            )
        
        if "transactions" in str(e):
            raise HTTPException(
                status_code=409,
                detail="Cannot delete account with transactions"
            )
        
    return