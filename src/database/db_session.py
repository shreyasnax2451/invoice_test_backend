from configs.env import *
from peewee import PostgresqlDatabase

db_params = {
    'database': DATABASE_NAME,
    'user':DATABASE_USER,
    'password':DATABASE_PASSWORD,
    'autorollback':True
}

class CustomDatabase(PostgresqlDatabase):
    def execute_sql(self, sql, params = None, commit = object()):
        if db.is_closed():
            db.connect(reuse_if_open=True)
        return super().execute_sql(sql, params, commit)

db = PostgresqlDatabase(**db_params)