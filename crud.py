from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Loan

async def create_loan(db: AsyncSession, amount: int, apr: int, term: int, status: str, owner_id: int):
    new_loan = Loan(amount=amount, apr=apr, term=term, status=status, owner_id=owner_id)
    db.add(new_loan)
    await db.commit()
    await db.refresh(new_loan)
    return new_loan

async def get_loans(db: AsyncSession, user_id: int):
    result = await db.execute(select(Loan).where(Loan.owner_id == user_id))
    return result.scalars().all()