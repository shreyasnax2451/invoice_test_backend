from database.db_session import db

def create_tables(Models):
    try:
        db.create_tables(Models)
        db.close()
        print('Tables Created')
    except Exception as e:
        print(e)
        raise