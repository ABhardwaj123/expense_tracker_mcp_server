from ..db.session import SessionLocal
from ..db import repository
from ..utils.categorizer import guess_category
from datetime import date 
import calendar



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


def check_budget_status(category=None , month=None , year=None):
    session = SessionLocal()

    today = date.today()
    if month is None:
        month = today.month
    if year is None:
        year = today.year


    if category is not None:
        category_id = repository.create_category(session, category)
    else:
        category_id = None

    budget = repository.get_budget(session, category_id, month, year)

    if budget is None:
        session.close()
        return {"message": f"No budget set for {category or 'overall'} in {month}/{year}"}

    first_day_of_month = date(year, month, 1)
    expenses = get_expenses(category=category, start_date=first_day_of_month, end_date=today, limit=100000)
    spent_so_far = sum(expense["amount"] for expense in expenses)

    days_elapsed = today.day
    _, days_in_month = calendar.monthrange(year, month)

    projected_total = (spent_so_far / days_elapsed) * days_in_month
    on_track = projected_total <= budget.monthly_budget

    result = {
        "category": category,
        "budget": budget.monthly_budget,
        "spent_so_far": spent_so_far,
        "projected_total": round(projected_total, 2),
        "on_track": on_track,
    }