from models.product import Product
from models.transaction import Transaction
from models.user import User
from models.contract import Contract
from database import DB


def logTransactionToAdmin(func):
        
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        print("Logging to Admin")
    return wrapper

def logTransactionToUser(func):
        
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        print("Logging to User")

    return wrapper

def logTransactionToDeepaDebug(func):
        
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        print("Logging to Deepa Debug")

    return wrapper

def logTransactionToAll(func):
    
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        logTransactionToDeepaDebug(func)(*args, **kwargs)
        logTransactionToAdmin(func)(*args, **kwargs)
        logTransactionToUser(func)(*args, **kwargs)

    return wrapper

class Manager:

    def __init__(self) -> None:
        pass

    @logTransactionToAll
    def createProduct(self, product:Product, user:User) -> dict:
        pass

    @logTransactionToAll
    def getProductHandle(self, productID:str, user:User) -> Product:
        pass

    @logTransactionToAll
    def getProductLink(self, productID:str, user:User) -> Product:
        pass

    @logTransactionToAll
    def initiateProductTransaction(self, productID:str, user:User) -> Transaction:
        pass

    @logTransactionToAll
    def checkUserAccount(self, user:User) -> bool:
        return False
    
    @logTransactionToAll
    def createAccount(self, user:User) -> User:
        pass

    @logTransactionToAll
    def chargeUserAccount(self, user:User) -> Transaction:
        pass
    
    @logTransactionToAll
    def fundProductContract(self, contract:Contract, user:User) -> Transaction:
        pass

    @logTransactionToAll
    def updateContractFufillment(self, contract:Contract, user:User) -> Contract:
        pass


if __name__ == "__main__":
    # manager = Manager()
    # manager.getProductLink("67")
    pass