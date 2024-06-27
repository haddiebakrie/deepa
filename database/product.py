import urllib.parse
from database.schema import DBSchema
from database.decorators import db_error_handler
from models.product import ProductInDB, productFromTuple
import json
import urllib

class ProductDB(DBSchema):

    @db_error_handler
    def createProduct(self, product):
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO "product"
                    (userID, storeID, productID, productTitle, productAmount, productDescription, metadata)
                    VALUES(%s, %s, %s, %s, %s, %s, %s)
                """,
                    (
                        product.userID,
                        product.storeID,
                        product.productID,
                        product.productTitle,
                        product.productAmount,
                        product.productDescription,
                        json.dumps(product.metadata),
                    ),
                )
                conn.commit()
                return self.getProduct(productID=product.productID)

    @db_error_handler
    def getProduct(self, productID):
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM "product"
                    WHERE productID=%s AND deletedAt IS NULL
                """, (productID,),
                )

                result = cursor.fetchone()

                if result:
                    return productFromTuple(result)
                
    @db_error_handler
    def updateProduct(self, productID, key, value):
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"""
                    UPDATE "product"
                    SET {key}=%s
                    WHERE productID=%s AND deletedAt IS NULL
                """, (value, productID),
                )
                conn.commit()

                return self.getProduct(productID)
            
    @db_error_handler
    def deleteProduct(self, productID):
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"""
                    UPDATE "product"
                    SET deletedAt=CURRENT_TIMESTAMP 
                    WHERE productID=%s AND deletedAt IS NULL
                """, (productID, ),
                )
                conn.commit()

                return
            
    @db_error_handler
    def getProductURL(self, productID):
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM "product"
                    WHERE productID=%s AND deletedAt IS NULL
                """, (productID, ),
                )

                result = cursor.fetchone()

                if result:
                    p = productFromTuple(result)
                    return f"https://deepastore/u{p.storeID}/{urllib.parse.quote_plus(p.productTitle.lower())}"
