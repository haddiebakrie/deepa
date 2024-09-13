from pydantic import BaseModel


class Transaction(BaseModel):
    pass

class TransactionInDB(Transaction):
    pass