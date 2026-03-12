from fastapi import (
    APIRouter, 
    Depends, 
    HTTPException)
from sqlalchemy.orm import Session

from app.modules.transactions.schemas import TransactionCreate
from app.modules.transactions.service import (
    create_transaction, 
    get_all_transactions,
    delete_transaction)
from app.db.session import SessionLocal

router = APIRouter()

# This function creates a db session
# Every request gets its own session
def get_db():
    db = SessionLocal()

    try:
        yield db    # returns the db session to FastAPI
    
    finally:
        db.close()  # always close the connection


@router.get("/transactions")
def get_transactions(db: Session = Depends(get_db)):

    transactions = get_all_transactions(db)

    # Convert db objects into safe response format
    return [
        {
            "id": transaction.id.hex(),
            "account_id": transaction.account_id.hex(),
            "amount": transaction.amount,
            "description": transaction.description,
            "transaction_type": transaction.transaction_type
        }
        for transaction in transactions
    ]



# POST endpoint to create a new transaction
@router.post("/transactions")
def create_transaction_endpoint(
    transaction: TransactionCreate,               
    db: Session = Depends(get_db)):   

    account_bytes = bytes.fromhex(transaction.account_id)

    # Call service layer
    new_transaction = create_transaction(
        db,
        account_bytes,
        transaction.amount,
        transaction.description,
        transaction.transaction_type
    )

    # Return safe response
    return {
        "amount": new_transaction.amount
    }


# DELETE endpoint to delete a transaction
@router.delete("/transactions/{transaction_id}")
def delete_transaction_endpoint(
    transaction_id: str,
    db: Session = Depends(get_db)):

    try:
        transaction_bytes = bytes.fromhex(transaction_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid transaction id format"
        )

    if len(transaction_bytes) != 16:
        raise HTTPException(
            status_code=400,
            detail="Invalid transaction id format"
        )

    try:
        delete_transaction(db, transaction_bytes)

    except ValueError as e:
        if "not found" in str(e):
            raise HTTPException(
                status_code=404, 
                detail="Transaction not found"
            )
    
    return