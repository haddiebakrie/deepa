import urllib.parse
from models.payment import paymentFromTuple
from database.schema import DBSchema
from database.decorators import db_error_handler
from models.contract import ContractInDB, contractFromTuple
import json
import urllib

class ContractDB(DBSchema):

    @db_error_handler
    def createContract(self, contract):
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT userID FROM "product" 
                    WHERE (productID=%s OR text(id)=%s) AND deletedAt IS NULL
                """, (contract.productID, contract.productID))

                uid = cursor.fetchone()[0]

                cursor.execute(
                    """
                    INSERT INTO "contract"
                    (contractID, contractTitle, sellerID, buyerID, productID, contractDescription, metadata)
                    VALUES(%s, %s, %s, %s, %s, %s, %s)
                """,
                    (
                        contract.contractID,
                        contract.contractTitle,
                        uid,
                        contract.buyerID,
                        contract.productID,
                        contract.contractDescription,
                        json.dumps(contract.metadata),
                    ),
                )
                conn.commit()
                return self.getContract(contractID=contract.contractID)

    @db_error_handler
    def getContract(self, contractID):
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM "contract"
                    WHERE (contractID=%s OR text(id)=%s) AND deletedAt IS NULL
                """, (contractID, contractID),
                )

                result = cursor.fetchone()

                if result:
                    return contractFromTuple(result)
                
    @db_error_handler
    def getPayments(self, contractID):
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM "payment"
                    WHERE contractID=%s AND deletedAt IS NULL
                """, (contractID, ),
                )

                result = cursor.fetchall()

                if result:
                    payments = [paymentFromTuple(x) for x in result]
                    return payments
                
    @db_error_handler
    def updateContract(self, contractID, key, value):
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"""
                    UPDATE "contract"
                    SET {key}=%s
                    WHERE (contractID=%s OR text(id)=%s) AND deletedAt IS NULL
                """, (value, contractID, contractID),
                )
                conn.commit()

                return self.getContract(contractID)
            
    @db_error_handler
    def deleteContract(self, contractID):
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"""
                    UPDATE "contract"
                    SET deletedAt=CURRENT_TIMESTAMP 
                    WHERE (contractID=%s OR text(id)=%s) AND deletedAt IS NULL
                """, (contractID, contractID),
                )
                conn.commit()

                return