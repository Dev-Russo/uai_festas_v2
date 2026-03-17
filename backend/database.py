from config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

"""
This module is responsible for setting up the database connection and creating the necessary objects for interacting with the database. It uses SQLAlchemy to create an engine, a session local, and a base class for the models. The database URL is loaded from the environment variables using the settings object from the config module. The engine is created using the create_engine function from SQLAlchemy, and the session local is created using the sessionmaker function. The base class is created using the declarative_base function, which allows us to define our models as classes that inherit from this base class. This module is essential for the proper functioning of the application, as it provides the necessary tools for interacting with the database and performing CRUD operations on the models.
"""

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()