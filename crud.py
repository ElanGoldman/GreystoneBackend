from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Loan, Share

async def create_loan(db: AsyncSession, amount: int, apr: int, term: int, status: str, owner_id: int):
    new_loan = Loan(amount=amount, apr=apr, term=term, status=status, owner_id=owner_id)
    db.add(new_loan)
    await db.commit()
    await db.refresh(new_loan)
    return new_loan

async def get_loans(db: AsyncSession, user_id: int):
    shares = await db.execute(select(Share.loan_id).where(Share.user_id == user_id))
    result = await db.execute(select(Loan).where((Loan.owner_id == user_id) | (Loan.id.in_([share[0] for share in shares]))))
    return result.scalars().all()

async def get_all_loans_temp(db: AsyncSession):
    result = await db.execute(select(Loan))
    return result.scalars().all()

async def get_all_shares_temp(db: AsyncSession):
    result = await db.execute(select(Share))
    return result.scalars().all()
 
async def create_share(db: AsyncSession, loan_id: int, owner_id: int, user_id: int):
    new_share = Share(loan_id=loan_id, owner_id=owner_id, user_id=user_id)
    db.add(new_share)
    await db.commit()
    await db.refresh(new_share)
    return {"message": "success!"}

async def get_schedule(db: AsyncSession, loan_id: int):
    loan = (await db.execute(select(Loan).where(Loan.id == loan_id))).scalars().first()
    if loan is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return amrotize(loan)

async def get_month(db: AsyncSession, loan_id: int, month: int):
    loan = (await db.execute(select(Loan).where(Loan.id == loan_id))).scalars().first()
    if loan is None:
        raise HTTPException(status_code=404, detail="Item not found")
    schedule = amrotize(loan)[month]
    return {}

def amrotize (loan):
    p = loan.amount
    r = loan.apr / 100 / 12
    n = loan.term
    monthly_payment = round((p * r) / (1 - ((1 + r) ** (-n))))
    payments = []
    for i in range(1, n):
        interest = round(p * r)
        p += interest - monthly_payment
        payments.append({"month": i,  "monthly_payment": monthly_payment, "remaining_balance": p})

    payments.append({"month": n,  "monthly_payment": round(p + p*r), "remaining_balance": 0})
    return payments
