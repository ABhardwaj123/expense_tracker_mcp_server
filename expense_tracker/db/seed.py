from ..config import DEFAULT_CATEGORIES
from .models import Category
from .session import SessionLocal


def seed_categories():

    session = SessionLocal()

    for category in DEFAULT_CATEGORIES:

        existing_category = session.query(Category).filter_by(name=category).first()

        if(existing_category is not None):
            continue

        new_category = Category(name=category , is_default=True)
        session.add(new_category)

    session.commit()
    session.close()


if __name__ == "__main__":
    seed_categories()
    print("seeded default categories")