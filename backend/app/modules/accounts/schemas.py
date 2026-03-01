# This file serves for acount input definition

from pydantic import BaseModel

# This schema represents the data  required to CREATE an account
class AccountCreate(BaseModel): 

    user_id: str          # which user owns this account
    name: str               # name of account
    account_type: str       # checking, savings, credit_card, loan
    balance: float          # Starting balance