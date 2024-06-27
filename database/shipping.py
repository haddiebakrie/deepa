import urllib.parse
from database.schema import DBSchema
from database.decorators import db_error_handler
from models.shipping import ShippingInDB, shippingFromTuple
import json
import urllib

class ShippingDB(DBSchema):

    @db_error_handler
    def createShipping(self, shipping):
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO "shipping"
                    (shippingID, shippingTitle, buyerID, contractID, shippingLocationID, shippingDescription, metadata)
                    VALUES(%s, %s, %s, %s, %s, %s, %s)
                """,
                    (
                        shipping.shippingID,
                        shipping.shippingTitle,
                        shipping.buyerID,
                        shipping.contractID,
                        shipping.shippingLocationID,
                        shipping.shippingDescription,
                        json.dumps(shipping.metadata),
                    ),
                )
                
                conn.commit()
                return self.getShipping(shippingID=shipping.shippingID)

    @db_error_handler
    def getShipping(self, shippingID):
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM "shipping"
                    WHERE (shippingID=%s OR text(id)=%s) AND deletedAt IS NULL
                """, (shippingID, shippingID),
                )

                result = cursor.fetchone()

                if result:
                    return shippingFromTuple(result)
                
    @db_error_handler
    def updateShipping(self, shippingID, key, value):
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"""
                    UPDATE "shipping"
                    SET {key}=%s
                    WHERE (shippingID=%s OR text(id)=%s) AND deletedAt IS NULL
                """, (value, shippingID, shippingID),
                )
                conn.commit()

                return self.getShipping(shippingID)
            
    @db_error_handler
    def deleteShipping(self, shippingID):
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"""
                    UPDATE "shipping"
                    SET deletedAt=CURRENT_TIMESTAMP 
                    WHERE (shippingID=%s OR text(id)=%s) AND deletedAt IS NULL
                """, (shippingID, shippingID),
                )
                conn.commit()

                return
            
