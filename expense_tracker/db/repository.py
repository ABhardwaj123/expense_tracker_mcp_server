from .session import SessionLocal
from .models import Category , Expense , Budget


#functions in which we have to query the database
#the data is collected from here and passed on to exepnse_service.py

def create_category(session , name , isDefault=False):
    
    existing_category = session.query(Category).filter_by(name=name).first()

    if(existing_category is not None):
        print("this category has already been created")
        return existing_category.id


    new_category = Category(name=name , is_default=isDefault)
    session.add(new_category)
    #sends pending sql statements to database but doesn't close the session
    #session is still open in case of rollback or something
    session.flush()
    
    print(f"{name} category is created")

    return new_category.id




def create_expense(session , amount , category_id , date , note=None):

    new_expense = Expense(
        amount=amount,
        category_id=category_id,
        note=note,
        date=date
    )

    session.add(new_expense)
    session.flush()

    print(f"new expense of {amount} added")

    return new_expense




def delete_expense(session , expense_id):

    expense = session.query(Expense).filter_by(id=expense_id).first()

    if expense is None:
        print("no such expense exists")
        return None

    session.delete(expense)
    return expense



def update_expense(session , expense_id , amount=None , category_id=None , note=None , date=None):

    expense = session.query(Expense).filter_by(id=expense_id).first()
    
    if expense is None:
        print("no such expense exists")
        return None

    if amount is not None:
        expense.amount = amount
    if category_id is not None:
        expense.category_id = category_id
    if note is not None:
        expense.note = note
    if date is not None:
        expense.date = date
 
    session.flush()
    return expense



def get_expenses(session , limit=10 , category_name=None , start_date=None , end_date=None):

    query = session.query(Expense)

    if category_name:
        query = query.filter(Expense.category.has(name=category_name))

    if start_date:
        query = query.filter(Expense.date >= start_date)

    if end_date:
        query = query.filter(Expense.date <= end_date)

    query = query.order_by(Expense.date.desc())
    query = query.limit(limit)

    expenses = query.all()

    return expenses




def set_budget(session , category_id , monthly_budget , month , year):

    existing_budget = session.query(Budget).filter_by(
        category_id=category_id , month=month , year=year
    ).first()

    if existing_budget is not None:
        existing_budget.monthly_budget = monthly_budget
        session.flush()
        return existing_budget

    new_budget = Budget(
        category_id=category_id , 
        monthly_budget=monthly_budget , 
        month=month , 
        year=year
    )

    session.add(new_budget)
    session.flush()
    return new_budget




def get_budget(session , category_id , month , year):

    budget = session.query(Budget).filter_by(
        category_id=category_id, month=month, year=year
    ).first()
    return budget
    