from sqlalchemy import Column , Integer , String , Boolean , Float , Date , DateTime , ForeignKey
from sqlalchemy.orm import declarative_base , relationship
from datetime import datetime


#Base is the parent class under which all tables are registered
Base = declarative_base()

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer , primary_key=True)
    name = Column(String , nullable=False , unique=True)
    is_default = Column(Boolean , nullable=False , default=False)



class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer , primary_key=True)
    amount = Column(Float, nullable=False)
    category_id = Column(Integer , ForeignKey("categories.id") , nullable=False)
    category = relationship("Category")
    # we will try to match by the best we can if nothing is given
    note = Column(String , nullable=True)
    date = Column(Date , nullable=False)
    created_at = Column(DateTime , default=datetime.now)



class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer , primary_key=True)
    category_id = Column(Integer , ForeignKey("categories.id") , nullable=True)
    monthly_budget = Column(Float , nullable=False)
    month = Column(Integer , nullable=False)
    year = Column(Integer , nullable=False)