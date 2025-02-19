from fastapi import FastAPI
import pyodbc 


conn = pyodbc.connect('DRIVER={SQL Server};SERVER=;DATABASE=;UID=;PWD=')


app = FastAPI(swagger_ui_parameters={"syntaxHighlight": {"theme": "obsidian"}})

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


@app.post("/loan")
def create_loan():
    return {"message": "Loan created successfully!"}

@app.get("/loan-schedule/{loan_id}")
def loan_schedule(loan_id: int):
    return {"message": f"Loan details for loan id: {loan_id}"}

@app.get("/loan-summary/{loan_id}/{month}")
def loan_summary(loan_id: int, month: int):
    return {"message": "Loan created successfully!"}

@app.get("/loans/{user_id}")
def get_loans(user_id: int):
    return {"message": f"Loans for user id: {user_id}"}

@app.get("/loans/{loan_id}/share/")
def share_loan(loan_id: int, owner_id: int, user_id: int):
    return {"message": f"Loan shared successfully!"}