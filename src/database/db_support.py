from database.db_session import db

def get_db():
    try:
        db.connect()
        yield db
    finally:
        if not db.is_closed():
            db.close()