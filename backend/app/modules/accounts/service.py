# Session represents a connection to the db
from sqlalchemy.orm import Session

#to calculate account balance from transactions
from sqlalchemy import func

from app.db.models.account import Account
from app.db.models.transaction import Transaction

def create_account(
    db: Session, 
    user_id: str, 
    name: str, 
    account_type: str, 
    balance: float):

    # Create a new Account object (this doesn't save yet)
    account = Account(
        user_id=bytes.fromhex(user_id), 
        name=name, 
        account_type=account_type, 
        balance=balance
    )

    db.add(account)        
    db.commit()        
    db.refresh(account)    

    return account         # returns the created account


# This function retrieves all users from the database
def get_all_accounts(db: Session):

    # Query means "ask the db for rows"
    accounts = db.query(Account).all()

    return accounts

def calculate_balance(db: Session, account_id: bytes):
    
    # Get starting balance from accounts table
    account = db.query(Account).filter(
        Account.id == account_id
    ).first()

    if account is None:
        return 0

    initial_balance = account.balance


    # Sum all transactions
    transactions_sum = db.query(
        func.sum(Transaction.amount)
    ).filter(
        Transaction.account_id == account_id
    ).scalar()


    if transactions_sum is None:
        transactions_sum = 0


    # Final balance
    return (initial_balance + transactions_sum)

def delete_account(db: Session, account_id: bytes):

    # Get account row
    account = db.query(Account).filter(
        Account.id == account_id
    ).first()
    
    if account is None:
        raise ValueError("Account not found")
    
    # Check if account has a transaction
    existing_transaction = db.query(Transaction).filter(
        Transaction.account_id == account_id
    ).first()

    if existing_transaction is not None:
        raise ValueError("Cannot delete account with transactions")
    
    db.delete(account)        
    db.commit()   