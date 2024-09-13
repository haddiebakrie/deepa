from datetime import datetime
from pydantic import BaseModel

class Shipping(BaseModel):
    shippingID: str
    shippingTitle: str
    buyerID: str
    contractID: str
    shippingLocationID: str
    shippingDescription: str = ""
    metadata:dict = {}

class ShippingInDB(Shipping):
    id: str = ""
    shippingStatus: str = ""
    createdAt: str = ""
    updatedAt: str = ""
    deletedAt: str = ""

def shippingFromTuple(db_tuple):
    return ShippingInDB(
        id=db_tuple[0],
        shippingTitle=db_tuple[1],
        shippingID=db_tuple[2],
        shippingDescription=db_tuple[3],
        shippingStatus=db_tuple[4],
        shippingLocationID=db_tuple[5],
        contractID=db_tuple[6],
        buyerID=db_tuple[7],
        createdAt=str(db_tuple[8]),
        updatedAt=str(db_tuple[9]),
        deletedAt=str(db_tuple[10]),
        metadata=db_tuple[11],
    )

class ShippingLocation(BaseModel):
    shippingLocationID: str
    state: str
    cities: list
    shippingNote: str
    shippingDuration: str
    shippingAmount: str
    storeID: str
    metadata:dict = {}

class ShippingLocationInDB(ShippingLocation):
    id: str = ""
    createdAt: str = ""
    updatedAt: str = ""
    deletedAt: str = ""

def shippingLocationFromTuple(db_tuple):
    return ShippingLocationInDB(
        id=db_tuple[0],
        shippingLocationID=db_tuple[1],
        state=db_tuple[2],
        cities=db_tuple[3],
        shippingNote=db_tuple[4],
        shippingDuration=db_tuple[5],
        shippingAmount=db_tuple[6],
        storeID=db_tuple[7],
        createdAt=str(db_tuple[8]),
        updatedAt=str(db_tuple[9]),
        deletedAt=str(db_tuple[10]),
        metadata=db_tuple[11],
    )
