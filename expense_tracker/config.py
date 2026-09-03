import os

DATABASE_URL = os.environ.get("DATABASE_URL" , "sqlite:///expense_tracker.db")

DEFAULT_CATEGORIES = [
    "food" , "transport" , "bills" , "shopping" , "entertainment" , "health" , "miscellaneous"
]