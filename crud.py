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
    return new_share
    #return {"message": "success!"}