from datetime import datetime
from pydantic import BaseModel


class Payment(BaseModel):
    paymentID: str
    amount: float
    contractID: str
    metadata:dict = {}

class PaymentInDB(Payment):
    id: str = ""
    createdAt: str = ""
    updatedAt: str = ""
    deletedAt: str = ""


def paymentFromTuple(db_tuple):
    return PaymentInDB(
        id=db_tuple[0],
        paymentID=db_tuple[1],
        contractID=db_tuple[2],
        amount=db_tuple[3],
        createdAt=str(db_tuple[4]),
        updatedAt=str(db_tuple[5]),
        deletedAt=str(db_tuple[6]),
        metadata=db_tuple[7],
    )
