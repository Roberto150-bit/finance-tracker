# Session represents a connection to the db
from sqlalchemy.orm import Session

# Imports the User table model
from app.db.models.account import Account

def create_account(
    db: Session, 
    user_id: bytes, 
    name: str, 
    account_type: str, 
    balance: float):

    # Create a new Account object (this doesn't save yet)
    account = Account(
        user_id=user_id, 
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
