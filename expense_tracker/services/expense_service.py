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



def get_expenses(limit=10 , category=None , start_date=None , end_date=None):
    session = SessionLocal()

    expenses = repository.get_expenses(session , limit , category , start_date , end_date)

    result = []

    for expense in expenses:
        result.append({
            "id": expense.id,
            "amount": expense.amount,
            "category": expense.category.name,
            "note": expense.note,
            "date": expense.date,
        })

    session.close()
    return result




def get_summary(start_date=None , end_date=None , group_by=None):
    expenses = get_expenses(limit=10000 , start_date=start_date , end_date=end_date)

    if group_by:

        totals_by_category = {}

        for expense in expenses:
            category_name = expense["category"]
            amount = expense["amount"]

            if category_name not in totals_by_category:
                totals_by_category[category_name] = 0

            totals_by_category[category_name] += amount

        return totals_by_category

    else:
        total = sum(expense["amount"] for expense in expenses)
        return {"total": total}




def set_budget(category=None, monthly_budget=None, month=None, year=None):
    session = SessionLocal()

    if category is not None:
        category_id = repository.create_category(session, category)
    else:
        category_id = None

    if month is None or year is None:
        today = date.today()
        month = today.month
        year = today.year

    budget = repository.set_budget(session, category_id, monthly_budget, month, year)

    result = {
        "category": category,
        "monthly_budget": budget.monthly_budget,
        "month": budget.month,
        "year": budget.year,
    }

    session.commit()
    session.close()
    return result