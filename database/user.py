import random
import urllib.parse
from database.schema import DBSchema
from database.decorators import db_error_handler
from models.user import UserInDB, userFromTuple
import json
import os
from dotenv import load_dotenv
import urllib
from database.store import StoreDB
from models.store import Store
load_dotenv()


class UserDB(DBSchema):

    @db_error_handler
    def createUser(self, user):
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO "user"
                    (userID, phone, passwordHash, metadata)
                    VALUES(%s, %s, %s, %s)
                """,
                    (
                        user.userID,
                        user.phone,
                        user.passwordHash,
                        json.dumps(user.metadata),
                    ),
                )
                conn.commit()
                user = self.getUser(userID=user.userID)
                store = Store(
                    userID=user.id, storeID="1", handle=user.phone, storeTitle="Default", storeDescription="My First Store"
                )
                StoreDB().createStore(store)
                return self.getUser(userID=user.userID)

    @db_error_handler
    def getUser(self, userID):
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM "user"
                    WHERE (userID=%s OR phone=%s) AND deletedAt IS NULL
                """,
                    (userID, userID),
                )

                result = cursor.fetchone()

                if result:
                    return userFromTuple(result)

    @db_error_handler
    def updateUser(self, userID, key, value):
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"""
                    UPDATE "user"
                    SET {key}=%s
                    WHERE userID=%s AND deletedAt IS NULL
                """,
                    (value, userID),
                )
                conn.commit()

                return self.getUser(userID)

    @db_error_handler
    def deleteUser(self, userID):
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"""
                    UPDATE "user"
                    SET deletedAt=CURRENT_TIMESTAMP 
                    WHERE userID=%s AND deletedAt IS NULL
                """,
                    (userID,),
                )
                conn.commit()

                return

    @db_error_handler
    def getUserURL(self, userID):
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM "user"
                    WHERE userID=%s AND deletedAt IS NULL
                """,
                    (userID,),
                )

                result = cursor.fetchone()

                if result:
                    p = userFromTuple(result)
                    return f"https://deepauser/{p.userID}"


    @db_error_handler
    def updateUserMetadata(self, userID: str, metadata):
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT metadata FROM "user" 
                    WHERE userID=%s AND deletedAt IS NULL
                """,
                    (userID,),
                )

                oldDict: dict = cursor.fetchone()[0]
                oldDict.update(metadata)
                cursor.execute(
                    """
                    UPDATE "user"
                    SET metadata=%s
                    WHERE userID=%s AND deletedAt IS NULL
                """,
                    (json.dumps(oldDict), userID),
                )
                conn.commit()

                return self.getUser(userID)
