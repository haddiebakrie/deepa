from datetime import datetime
from pydantic import BaseModel


class Product(BaseModel):
    userID: str = ""
    productID: str = ""
    productTitle: str
    productAmount: str
    storeID: str = ""
    productDescription: str = ""
    metadata:dict = {}


class ProductInDB(Product):
    id: str = ""
    createdAt: str = ""
    updatedAt: str = ""
    deletedAt: str = ""
    paidAmount: str = ""


def productFromTuple(db_tuple):
    return ProductInDB(
        id=db_tuple[0],
        productTitle=db_tuple[1],
        productAmount=db_tuple[2],
        productDescription=db_tuple[3],
        paidAmount=db_tuple[4],
        productID=db_tuple[5],
        userID=db_tuple[6],
        storeID=db_tuple[7],
        createdAt=str(db_tuple[8]),
        updatedAt=str(db_tuple[9]),
        deletedAt=str(db_tuple[10]),
        metadata=db_tuple[11],
    )
