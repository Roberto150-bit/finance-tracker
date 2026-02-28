from sqlalchemy import Column, String
from sqlalchemy.dialects.sqlite import BLOB
import uuid

from app.db.base import Base

class User(Base):

    __tablename__ = "users"

    id = Column(
        BLOB,
        primary_key=True,
        default=lambda: uuid.uuid4().bytes
    )

    email = Column(
        String,
        unique=True,
        index=True
    )

    password = Column(
        String
    )
