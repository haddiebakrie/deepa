import urllib.parse
from models.contract import contractFromTuple
from database.schema import DBSchema
from database.decorators import db_error_handler
from models.store import StoreInDB, storeFromTuple
from models.shipping import (
    ShippingLocation,
    ShippingLocationInDB,
    shippingLocationFromTuple,
)
from models.product import productFromTuple
import json
import os
from dotenv import load_dotenv
import urllib

load_dotenv()


class StoreDB(DBSchema):

    @db_error_handler
    def createStore(self, store):
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO "store"
                    (userID, storeID, handle, storeTitle, storeDescription, metadata)
                    VALUES(%s, %s, %s, %s, %s, %s)
                """,
                    (
                        store.userID,
                        store.storeID,
                        store.handle,
                        store.storeTitle,
                        store.storeDescription,
                        json.dumps(store.metadata),
                    ),
                )
                conn.commit()
                return self.getStore(store.storeID, store.userID)

    @db_error_handler
    def getStore(self, storeID, userID=None):
        with self.connect() as conn:
            with conn.cursor() as cursor:
                if not userID:
                    cursor.execute(
                    """
                    SELECT * FROM "store"
                    WHERE handle=%s AND deletedAt IS NULL
                """,
                    (storeID, ),
                )
                else:
                    cursor.execute(
                        """
                        SELECT * FROM "store"
                        WHERE userID=%s AND (storeID=%s OR handle=%s) AND deletedAt IS NULL
                    """,
                        (userID, storeID, storeID),
                    )

                result = cursor.fetchone()
                if result:
                    return storeFromTuple(result)

    @db_error_handler
    def getStores(self, userID=None):
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM "store"
                    WHERE userID=%s AND deletedAt IS NULL
                """,
                    (userID, ),
                )

                result = cursor.fetchall()
                if result:
                    result = [storeFromTuple(x) for x in result]
                    return result


    @db_error_handler
    def updateStore(self, storeID, key, value, userID=None,):
        store = self.getStore(storeID, userID)
        if store:
            storeID = store.id
            if not userID:
                userID = store.userID
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"""
                    UPDATE "store"
                    SET {key}=%s
                    WHERE storeID=%s AND userID=%s AND deletedAt IS NULL
                """,
                    (value, storeID, userID),
                )
                conn.commit()

                return self.getStore(storeID, userID)

    @db_error_handler
    def deleteStore(self, storeID, userID=None):
        store = self.getStore(storeID, userID)
        if store:
            storeID = store.id
            if not userID:
                userID = store.userID
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"""
                    UPDATE "store"
                    SET deletedAt=CURRENT_TIMESTAMP 
                    WHERE storeID=%s AND userID=%s AND deletedAt IS NULL
                """,
                    (storeID, userID),
                )
                conn.commit()

                return

    @db_error_handler
    def getStoreURL(self, storeID):
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM "store"
                    WHERE storeID=%s AND deletedAt IS NULL
                """,
                    (storeID,),
                )

                result = cursor.fetchone()

                if result:
                    p = storeFromTuple(result)
                    return f"https://deepastore/{p.handle}"

    @db_error_handler
    def getStoreProducts(self, storeID, userID=None, limit=50, offset=0):
        store = self.getStore(storeID, userID)
        if store:
            storeID = store.storeID
            if not userID:
                userID = store.userID
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM "product" 
                    WHERE text(storeID)=%s AND deletedAt IS NULL
                    LIMIT %s 
                    OFFSET %s
                """,
                    (storeID, limit, offset),
                )

                result = cursor.fetchall()

                if result:
                    productList = [productFromTuple(x) for x in result]
                    return productList

    @db_error_handler
    def getStoreAnalytics(self, storeID, userID=None, limit=10, offset=0):
        products = self.getStoreProducts(storeID, userID)
        sales = self.getStoreSales(storeID, userID)
        revenue = self.getStoreRevenue(storeID, userID)
        pending_orders = self.getStorePendingOrders(storeID, userID)
        return {
            "products": products,
            "sales": sales,
            "total revenue": revenue,
            "pending orders": len(pending_orders),
            "orders": pending_orders
        }

    @db_error_handler
    def getStoreFromURL(self, storeURL: str):
        handle = storeURL.replace(f"{os.environ['STORE_URL_DOMAIN']}", "")
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM "store" 
                    WHERE handle=%s AND deletedAt IS NULL
                """,
                    (handle,),
                )

                result = cursor.fetchone()

                if result:
                    return storeFromTuple(result)

    @db_error_handler
    def updateStoreMetadata(self, storeID: str, metadata, userID=None):
        store = self.getStore(storeID)
        if store:
            storeID = store.id
            if not userID:
                userID = store.userID
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT metadata FROM "store" 
                    WHERE storeID=%s AND deletedAt IS NULL
                """,
                    (storeID,),
                )

                oldDict: dict = cursor.fetchone()[0]
                oldDict.update(metadata)
                cursor.execute(
                    """
                    UPDATE "store"
                    SET metadata=%s
                    WHERE storeID=%s AND deletedAt IS NULL
                """,
                    (json.dumps(oldDict), storeID),
                )
                conn.commit()

                return self.getStore(storeID, userID)

    @db_error_handler
    def createShippingLocation(self, shippingLocation: ShippingLocation):
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO "shippingLocation"
                    (shippingLocationID, state, cities, shippingNote, shippingDuration, shippingAmount, storeID, metadata)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                    (
                        shippingLocation.shippingLocationID,
                        shippingLocation.state,
                        json.dumps(shippingLocation.cities),
                        shippingLocation.shippingNote,
                        shippingLocation.shippingDuration,
                        shippingLocation.shippingAmount,
                        shippingLocation.storeID,
                        json.dumps(shippingLocation.metadata),
                    ),
                )
                conn.commit()
                return self.getShippingLocation(
                    shippingLocationID=shippingLocation.shippingLocationID
                )

    @db_error_handler
    def getShippingLocation(self, shippingLocationID):
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM "shippingLocation"
                    WHERE shippingLocationID=%s AND deletedAt IS NULL
                """,
                    (shippingLocationID,),
                )

                result = cursor.fetchone()

                if result:
                    return shippingLocationFromTuple(result)
                
    @db_error_handler
    def getStoreRevenue(self, storeID, userID=None):
        store = self.getStore(storeID, userID)
        if store:
            storeID = store.id
            if not userID:
                userID = store.userID
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT paidAmount FROM "contract"
                    WHERE sellerID=%s AND deletedAt IS NULL
                """,
                    (userID,),
                )

                result = sum([x[0] for x in cursor.fetchall()])

                if result:
                    return result
        return 0
                
    @db_error_handler
    def getStorePendingOrders(self, storeID, userID=None):
        print(userID)
        store = self.getStore(storeID, userID)
        if store:
            storeID = store.id
            if not userID:
                userID = store.userID
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM "contract"
                    WHERE sellerID=%s AND fulfillmentStatus=%s AND deletedAt IS NULL
                """,
                    (userID, 'fulfilled'),
                )

                result = cursor.fetchall()

                contracts = [contractFromTuple(x) for x in result]

                if contracts:
                    return contracts
        return []
                
    @db_error_handler
    def getStoreSales(self, storeID, userID=None):
        store = self.getStore(storeID, userID)
        if store:
            storeID = store.id
            if not userID:
                userID = store.userID
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT paidAmount FROM "contract"
                    WHERE sellerID=%s AND deletedAt IS NULL
                """,
                    (userID,),
                )

                result = len(cursor.fetchall())

                if result:
                    return result
        return 0
