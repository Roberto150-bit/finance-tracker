from sqlalchemy import Column, String, Float, ForeignKey, DateTime
from sqlalchemy.dialects.sqlite import BLOB
import uuid
import datetime

from app.db.base import Base

# Represents a financial transaction
class Transaction(Base):

    __tablename__ = "transactions"

    # unique transaction ID
    id = Column(
        BLOB,
        primary_key=True,
        default=lambda: uuid.uuid4().bytes
    )

    # which account this belongs to
    account_id = Column(
        BLOB,
        ForeignKey("accounts.id")
    )

    # Positive = income
    # Negative = expense
    amount = Column(Float)

    # Example: "Groceries"
    description = Column(String)

    # When transaction happened
    date = Column(
        DateTime,
        default=datetime.datetime.utcnow
    )

    # income / expense / transfer (later)
    transaction_type = Column(String)