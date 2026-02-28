# main.py -> routes.py -> service.py -> models.py -> database
# routes - HTTP logic
# service - business logic
# models - database tables
# schemas - data shapes
# Client -> API -> Service -> Database

from fastapi import FastAPI
from app.modules.users.routes import router as users_router
from app.modules.accounts.routes import router as accounts_router
from app.modules.transactions.routes import router as transactions_router

from app.db.session import engine
from app.db.base import Base

# This imports models so tables exist
import app.db.models

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(users_router, prefix="/api/v1")
app.include_router(accounts_router, prefix="/api/v1")
app.include_router(transactions_router, prefix="/api/v1")