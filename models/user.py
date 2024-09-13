from datetime import datetime
from typing import Union
from pydantic import BaseModel


class User(BaseModel):
    userID: str
    phone: str
    passwordHash: str = ""
    metadata: dict

class UserInDB(User):
    id: str = ""
    createdAt: str = ""
    updatedAt: str = ""
    deletedAt: str = ""
    username:Union[str, None] = ""
    lastLogin:str = ""
    status:str = ""
    passwordHash:str = ""
    isVerified: bool = False


def userFromTuple(db_tuple):
    return UserInDB(
        id=db_tuple[0],
        userID=db_tuple[1],
        phone=db_tuple[2],
        username=db_tuple[3],
        passwordHash=db_tuple[4],
        isVerified=db_tuple[5],
        status=db_tuple[6],
        createdAt=str(db_tuple[7]),
        updatedAt=str(db_tuple[8]),
        deletedAt=str(db_tuple[9]),
        lastLogin=str(db_tuple[10]),
        metadata=db_tuple[11],
    )
