import psycopg2 as pg
from database.settings import TITLE, PG_PLAIN, PG_OBSCURE, PG_PORT, PG_HOST

class DB:

    def __init__(self, database=TITLE) -> None:
        self.database = database

    def welcome(self):
        print(f"Welcome to {TITLE}. You are connected to the database.\n")

    def connect(self):
        return pg.connect(database=self.database, user=PG_PLAIN, password=PG_OBSCURE, port=PG_PORT, host=PG_HOST)
