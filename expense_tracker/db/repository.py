from .session import SessionLocal
from .models import Category , Expense

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



    