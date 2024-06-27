import urllib.parse
from database.schema import DBSchema
from database.decorators import db_error_handler
from models.payment import PaymentInDB, paymentFromTuple
import json
import urllib

class PaymentDB(DBSchema):

    @db_error_handler
    def createPayment(self, payment):
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO "payment"
                    (paymentID, contractID, amount, metadata)
                    VALUES(%s, %s, %s, %s)
                """,
                    (
                        payment.paymentID,
                        payment.contractID,
                        payment.amount,
                        json.dumps(payment.metadata),
                    ),
                )
                cursor.execute(
                    f"""
                    SELECT productID FROM "contract"
                    WHERE (contractID=%s OR text(id)=%s) AND deletedAt IS NULL
                """, (payment.contractID, payment.contractID,),
                )
                pid = cursor.fetchone()[0]
                cursor.execute(
                    f"""
                    SELECT productAmount FROM "product"
                    WHERE (productID=text(%s) OR id=%s) AND deletedAt IS NULL
                """, (pid, pid),
                )
                pa = cursor.fetchone()[0]
                cursor.execute(
                    f"""
                    SELECT paidAmount FROM "contract"
                    WHERE (contractID=%s OR text(id)=%s) AND deletedAt IS NULL
                """, (payment.contractID, payment.contractID),
                )
                ca = cursor.fetchone()[0]
                newAmount = float(ca) + float(payment.amount)
                f = "partiallyFulfilled" if float(pa) > newAmount else "fulfilled"
                cursor.execute(
                    f"""
                    UPDATE "contract"
                    SET fulfillmentStatus=%s, paidAmount=%s
                    WHERE (contractID=%s OR text(id)=%s) AND deletedAt IS NULL
                """, (f, newAmount, payment.contractID, payment.contractID),
                )
                
                conn.commit()
                return self.getPayment(paymentID=payment.paymentID)

    @db_error_handler
    def getPayment(self, paymentID):
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM "payment"
                    WHERE (paymentID=%s OR text(id)=%s) AND deletedAt IS NULL
                """, (paymentID, paymentID),
                )

                result = cursor.fetchone()

                if result:
                    return paymentFromTuple(result)
                
    @db_error_handler
    def updatePayment(self, paymentID, key, value):
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"""
                    UPDATE "payment"
                    SET {key}=%s
                    WHERE (paymentID=%s OR text(id)=%s) AND deletedAt IS NULL
                """, (value, paymentID, paymentID),
                )
                conn.commit()

                return self.getPayment(paymentID)
            
    @db_error_handler
    def deletePayment(self, paymentID):
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"""
                    SELECT contractID FROM "payment"
                    WHERE (paymentID=%s OR text(id)=%s) AND deletedAt IS NULL
                """, (paymentID, paymentID),
                )
                cid = cursor.fetchone()[0]
                cursor.execute(
                    f"""
                    UPDATE "payment"
                    SET deletedAt=CURRENT_TIMESTAMP 
                    WHERE (paymentID=%s OR text(id)=%s) AND deletedAt IS NULL
                """, (paymentID, paymentID),
                )
                cursor.execute(
                    f"""
                    UPDATE "contract"
                    SET deletedAt=CURRENT_TIMESTAMP 
                    WHERE (contractID=%s OR text(id)=%s) AND deletedAt IS NULL
                """, (str(cid), str(cid)),
                )
                conn.commit()

                return
            
