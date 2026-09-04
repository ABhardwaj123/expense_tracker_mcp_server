import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    f"sqlite:///{os.path.join(BASE_DIR, 'expense_tracker.db')}"
)
DEFAULT_CATEGORIES = [
    "food" , "transport" , "bills" , "shopping" , "entertainment" , "health" , "others"
]