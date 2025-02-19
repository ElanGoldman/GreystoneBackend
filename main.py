from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from contextlib import asynccontextmanager
from pydantic import BaseModel

from crud import create_loan, get_loans, create_share, get_all_loans_temp, get_all_shares_temp, get_month, get_schedule
from database import init_db, close_db, get_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()  # Initialize database
    yield  # Continue running FastAPI
    await close_db()  # Properly close the database engine


app = FastAPI(lifespan=lifespan, swagger_ui_parameters={"syntaxHighlight": {"theme": "obsidian"}})


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

class Loan(BaseModel):
    amount: int
    apr: int
    term: int
    status: str
    owner_id: int
    
@app.post("/loan")
async def add_loan(loan: Loan, db: AsyncSession = Depends(get_db)):
    return await create_loan(db, loan.amount, loan.apr, loan.term, loan.status, loan.owner_id)

@app.get("/loan-schedule/{loan_id}")
async def loan_schedule(loan_id: int, db: AsyncSession = Depends(get_db)):
    return await get_schedule(db, loan_id)

@app.get("/loan-summary/{loan_id}/{month}")
async def loan_summary(loan_id: int, month: int, db: AsyncSession = Depends(get_db)):
    return await get_month(db, loan_id, month)

@app.get("/loans/all")
async def all_loans(db: AsyncSession = Depends(get_db)):
    return await get_all_loans_temp(db)

@app.get("/loans/{user_id}")
async def list_loans(user_id: int, db: AsyncSession = Depends(get_db)):
    return await get_loans(db, user_id)

@app.post("/loans/{loan_id}/share/")
async def share_loan(loan_id: int, owner_id: int, user_id: int, db: AsyncSession = Depends(get_db)):
    return await create_share(db, loan_id, owner_id, user_id)

@app.get("/shares/all")
async def all_shares(db: AsyncSession = Depends(get_db)):
    return await get_all_shares_temp(db)
