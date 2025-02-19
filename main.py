from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from contextlib import asynccontextmanager
from pydantic import BaseModel

from crud import create_loan, get_loans
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

# async def createLoan():
#     return await create_loan()

@app.get("/loan-schedule/{loan_id}")
def loan_schedule(loan_id: int):
    return {"message": f"Loan details for loan id: {loan_id}"}

@app.get("/loan-summary/{loan_id}/{month}")
def loan_summary(loan_id: int, month: int):
    return {"message": "Loan created successfully!"}

@app.get("/loans/{user_id}")
async def list_loans(user_id: int, db: AsyncSession = Depends(get_db)):
    return await get_loans(db, user_id)

@app.get("/loans/{loan_id}/share/")
def share_loan(loan_id: int, owner_id: int, user_id: int):
    return {"message": f"Loan shared successfully!"}