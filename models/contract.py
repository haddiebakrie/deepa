from datetime import datetime
from pydantic import BaseModel


class Contract(BaseModel):
    contractID: str
    contractTitle: str
    buyerID: str
    productID: str
    contractDescription: str = ""
    metadata:dict = {}


class ContractInDB(Contract):
    id: str = ""
    createdAt: str = ""
    updatedAt: str = ""
    deletedAt: str = ""
    fulfillmentStatus: str = ""
    sellerID: str = ""
    paidAmount: float = 0


def contractFromTuple(db_tuple):
    return ContractInDB(
        id=db_tuple[0],
        contractTitle=db_tuple[1],
        contractID=db_tuple[2],
        sellerID=db_tuple[3],
        buyerID=db_tuple[4],
        productID=db_tuple[5],
        fulfillmentStatus=db_tuple[6],
        contractDescription=db_tuple[7],
        paidAmount=str(db_tuple[8]),
        createdAt=str(db_tuple[9]),
        updatedAt=str(db_tuple[10]),
        deletedAt=str(db_tuple[11]),
        metadata=db_tuple[12],
    )
