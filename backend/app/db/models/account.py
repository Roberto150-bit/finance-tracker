from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.dialects.sqlite import BLOB
import uuid

from app.db.base import Base

# Represents a financial account
# Examples:
# - Checking
# - Savings
# - Credit Card
# - Loan
class Account(Base):

    __tablename__ = "accounts"

    # Unique account ID
    id = Column(
        BLOB,
        primary_key=True,
        default=lambda: uuid.uuid4().bytes
    )

    # Owner of account
    user_id = Column(
        BLOB,
        ForeignKey("users.id")
    )

    # Example:
    # "Chase Checking"
    name = Column(String)

    # checking, savings, credit_card, loan
    account_type = Column(String)

    # Current balance
    balance = Column(Float)
