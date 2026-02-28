# This file serves for user input definition


# Pydantic BaseModel is used to define the structure of data
from pydantic import BaseModel

# This schema represents the data  required to CREATE a user
class UserCreate(BaseModel):

    email: str
    password: str