# creating an engine that is actually a connection to sqlite file

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
from ..config import DATABASE_URL

#engine is the actual object that knows how to connect and communicate with database
engine = create_engine(DATABASE_URL)

#Base.metadata stores the actual schema information from every class that inherited from Base
#this tell that using this engine , go and create every table in Base if it doesn't exist
Base.metadata.create_all(engine)

#SessionLocal is a factory that hands you a fresh session with DB when you need to read/write data
SessionLocal = sessionmaker(bind=engine)