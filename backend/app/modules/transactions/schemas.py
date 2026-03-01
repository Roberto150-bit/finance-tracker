# Pydantic BaseModel is used to define the structure of data
from pydantic import BaseModel

# This schema represents the data  required to CREATE a user
class TransactionCreate(BaseModel):

    account_id: str
    amount: float
    description: str
    transaction_type: str
