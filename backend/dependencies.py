from database import SessionLocal

"""
    This function is a dependency that provides a database session to the routes that require it. It creates a new session using the SessionLocal class from the database module, yields it to the caller, and then closes the session after the request is completed. This allows us to use the same session for multiple requests without having to create a new one for each request, which can improve performance and reduce resource usage. By using this dependency in our routes, we can easily access the database and perform CRUD operations on our models without having to worry about managing the database connection ourselves.
"""

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()