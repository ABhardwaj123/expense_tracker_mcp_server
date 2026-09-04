from ..db.session import SessionLocal
from ..db import repository
from ..utils.categorizer import guess_category
from datetime import date 



def add_expense(amount , note=None , category=None , expense_date=None):

    session = SessionLocal()

    if category is not None:
        category_name = category
    else:
        category_name = guess_category(note)

    category_id = repository.create_category(session , category_name)

    if expense_date is None:
        expense_date = date.today()

    new_expense = repository.create_expense(session , amount , category_id , expense_date , note)

    session.commit()

    result = {
        "amount": new_expense.amount,
        "category": category_name,                      
        "date": new_expense.date,
        "note": new_expense.note,
    }

    session.close()
    return result



def edit_expense(expense_id , amount=None , category=None , note=None , expense_date=None):
    session = SessionLocal()

    if category is not None:
        category_id = repository.create_category(session, category)
    else:
        category_id = None

    edited_expense = repository.update_expense(session , expense_id , amount , category_id , note , expense_date)

    if edited_expense is None:
        session.close()
        return {"success": False , "message": f"No expense found with id {expense_id}"}


    result = {
        "success": True,
        "amount": edited_expense.amount,
        "note": edited_expense.note,
    }

    session.commit()
    session.close()
    return result





def delete_expense(expense_id):
    session = SessionLocal()

    deleted = repository.delete_expense(session, expense_id)

    if deleted is None:
        session.close()
        return {"success": False, "message": f"No expense found with id {expense_id}"}

    result = {
        "success": True,
        "amount": deleted.amount,
        "note": deleted.note,
    }

    session.commit()
    session.close()
    return result