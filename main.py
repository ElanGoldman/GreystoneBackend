from fastapi import FastAPI
import sqlite3 
import asyncio
from contextlib import asynccontextmanager
from crud import create_loan, get_loans


from database import init_db, close_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()  # Initialize database
    yield  # Continue running FastAPI
    await close_db()  # Properly close the database engine


app = FastAPI(lifespan=lifespan, swagger_ui_parameters={"syntaxHighlight": {"theme": "obsidian"}})


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


@app.post("/loan")
async def add_loan(amount: int, apr: int, term: int, status: str, owner_id: int):
    return await create_loan(amount, apr, term, status, owner_id)

# async def createLoan():
#     return await create_loan()

@app.get("/loan-schedule/{loan_id}")
def loan_schedule(loan_id: int):
    return {"message": f"Loan details for loan id: {loan_id}"}

@app.get("/loan-summary/{loan_id}/{month}")
def loan_summary(loan_id: int, month: int):
    return {"message": "Loan created successfully!"}

@app.get("/loans/{user_id}")
async def get_loans(user_id: int):
    return await get_loans(user_id)

@app.get("/loans/{loan_id}/share/")
def share_loan(loan_id: int, owner_id: int, user_id: int):
    return {"message": f"Loan shared successfully!"}