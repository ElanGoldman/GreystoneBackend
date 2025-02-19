from sqlalchemy.orm import DeclarativeBase  # Corrected import
from sqlalchemy import Column, Integer, String

# Define the base class
class Base(DeclarativeBase):
    pass  # Required for the new SQLAlchemy version

# Define the Loan model
class Loan(Base):
    __tablename__ = "loans"
    
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, nullable=False)
    apr = Column(Integer, nullable=False)
    term = Column(Integer, nullable=False)
    status = Column(String, nullable=False)
    owner_id = Column(Integer, nullable=False)

# Define the Share model
class Share(Base):
    __tablename__ = "shares"
    
    id = Column(Integer, primary_key=True, index=True)
    loan_id = Column(Integer, nullable=False)
    owner_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
