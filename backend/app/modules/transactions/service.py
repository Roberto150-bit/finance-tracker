from sqlalchemy.orm import Session
# Imports the Transaction table model
from app.db.models.transaction import Transaction


def create_transaction(
    db: Session, 
    account_id: bytes,
    amount: float,
    description: str,
    transaction_type: str):

    # Create a new Transaction object (this doesn't save yet)
    transaction = Transaction(
        account_id=account_id,
        amount=amount,
        description=description,
        transaction_type=transaction_type
    )

    
    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return transaction


# This function retrieves all transactions from the database
def get_all_transactions(db: Session):

    # Query means "ask the db for rows"
    transactions = db.query(Transaction).all()

    return transactions