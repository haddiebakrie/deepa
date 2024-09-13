from psycopg2 import sql
from database.connection import DB
from database.decorators import db_error_handler
from database.settings import TITLE

class DBOperations(DB):

    @db_error_handler
    def createSandboxDB(self, name):
        conn = self.connect()
        conn.autocommit = True
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    sql.SQL("""
                        CREATE DATABASE {name}
                        WITH OWNER = postgres
                        ENCODING = 'UTF8'
                        CONNECTION LIMIT = -1
                        IS_TEMPLATE = False;
                    """).format(name=sql.Identifier(name))
                )
        finally:
            conn.close()

    @db_error_handler
    def createUserSandbox(self, user, password):
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    sql.SQL("""
                        CREATE ROLE {user} WITH
                        LOGIN NOSUPERUSER CREATEDB NOCREATEROLE
                        INHERIT NOREPLICATION CONNECTION LIMIT -1
                        PASSWORD %s;
                    """).format(user=sql.Identifier(user)),
                    [password]
                )
                self.activateSandboxRole(user, conn)
                conn.commit()

    @db_error_handler
    def activateSandboxRole(self, user, conn):
        with conn.cursor() as cursor:
            cursor.execute(
                sql.SQL("""
                    GRANT CONNECT ON DATABASE {dbname} TO {user};
                """).format(user=sql.Identifier(user), dbname=sql.Identifier(TITLE))
            )

    @db_error_handler
    def promoteUser(self, user):
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    sql.SQL("""
                        ALTER ROLE {user} SUPERUSER REPLICATION;
                    """).format(user=sql.Identifier(user))
                )
                conn.commit()
