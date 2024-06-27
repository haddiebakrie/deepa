from datetime import datetime
from pydantic import BaseModel


class Store(BaseModel):
    userID: str = ""
    storeID: str = ""
    handle: str = ""
    storeTitle: str = ""
    storeDescription: str = ""
    metadata:dict = {}

class StoreInDB(Store):
    id: str = ""
    createdAt: str = ""
    updatedAt: str = ""
    deletedAt: str = ""

def storeFromTuple(db_tuple):
    return StoreInDB(
        id=db_tuple[0],
        handle=db_tuple[1],
        storeID=db_tuple[2],
        storeDescription=db_tuple[3],
        storeTitle=db_tuple[4],
        userID=db_tuple[5],
        createdAt=str(db_tuple[6]),
        updatedAt=str(db_tuple[7]),
        deletedAt=str(db_tuple[8]),
        metadata=db_tuple[9],
    )
