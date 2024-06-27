import random
from database.product import ProductDB
from database.store import StoreDB
from database.contract import ContractDB
from database.payment import PaymentDB
from database.user import UserDB
from database.shipping import ShippingDB
import uuid, json, unittest
from models.product import Product, ProductInDB
from models.store import Store, StoreInDB
from models.shipping import ShippingLocation, ShippingLocationInDB, ShippingInDB, Shipping
from models.contract import Contract, ContractInDB
from models.payment import Payment, PaymentInDB
from models.user import User, UserInDB
from dotenv import load_dotenv
import os

load_dotenv()


class ProductTest(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.db = ProductDB("DeepaTest")
        self.db.initializeSchema()

    def testProductCRUD(self):
        product = Product(
            userID="1",
            productID=str(uuid.uuid4()),
            storeID="1",
            productTitle=f"Test Product {str(uuid.uuid4())}: White floral Ankara",
            productAmount=10000,
        )
        v1 = self.db.createProduct(product)
        assert type(v1) == ProductInDB

        v2 = self.db.getProduct(v1.productID)
        assert v2.productTitle == v1.productTitle

        v3 = self.db.updateProduct(
            v1.productID, "metadata", json.dumps({"material": "ankara"})
        )
        assert v3.metadata == {"material": "ankara"}

        self.db.deleteProduct(v1.productID)
        v4 = self.db.getProduct(v1.productID)
        assert type(v4) == type(None)

    def testProductLink(self):
        product = Product(
            userID="1",
            productID=str(uuid.uuid4()),
            storeID="1",
            productTitle=f"Test Product",
            productAmount=10000,
        )
        v1 = self.db.createProduct(product)
        v2 = self.db.getProductURL(v1.productID)
        assert v2 == f"{os.environ['STORE_URL_DOMAIN']}u1/test+product"


class StoreTest(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.db = StoreDB("DeepaTest")

    def testStoreCRUD(self):
        unq = str(uuid.uuid4())
        store = Store(
            userID="1",
            storeID=str(uuid.uuid4()),
            handle=f"test{unq}",
            storeTitle=f"Test Store {unq}: Kajora",
            storeDescription="A B2B store",
        )
        v1 = self.db.createStore(store)
        assert type(v1) == StoreInDB

        v2 = self.db.getStore(v1.storeID)
        assert v2.handle == v1.handle

        v3 = self.db.updateStore(
            v1.storeID, "metadata", json.dumps({"phone": "2349049500328"})
        )
        assert v3.metadata == {"phone": "2349049500328"}

        self.db.deleteStore(v1.storeID)
        v4 = self.db.getStore(v1.storeID)
        assert type(v4) == type(None)

    def testStoreLink(self):
        unq = str(uuid.uuid4())
        store = Store(
            userID="1",
            storeID=str(uuid.uuid4()),
            handle=f"test{unq}",
            storeTitle=f"Test Store {unq}: Kajora",
            storeDescription="A B2B store",
        )
        v1 = self.db.createStore(store)
        v2 = self.db.getStoreURL(v1.storeID)
        assert v2 == f"{os.environ['STORE_URL_DOMAIN']}test{unq}"

    def testGetStoreProducts(self):
        v2 = self.db.getStoreProducts("testd8bbb762-750c-484e-b996-2ee4a8ea9193")
        assert type(v2) == list

    def testGetStoreFromURL(self):
        v1 = self.db.getStoreFromURL(f"{os.environ['STORE_URL_DOMAIN']}testd8bbb762-750c-484e-b996-2ee4a8ea9193")
        assert type(v1) == StoreInDB

    def testUpdateStoreMetadata(self):
        v1 = self.db.updateStoreMetadata("251b699d-87d2-42c8-89fc-a42ff05aab6e", {"owner": "haddy"})
        assert v1.metadata.get("owner", False) and v1.metadata.get("phone", False)

    def testCreateStoreShippingLocation(self):
        unq = str(uuid.uuid4())
        loc = ShippingLocation(
            shippingLocationID=unq,
            storeID="1",
            state="Lagos",
            cities=["Mainland"],
            shippingNote="Delivery can take longer due to traffic",
            shippingDuration=7,
            shippingAmount=3000,
        )
        v1 = self.db.createShippingLocation(loc)
        assert type(v1) == ShippingLocationInDB

class UserTest(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.db = UserDB("DeepaTest")

    def testUserCRUD(self):
        unq = str(uuid.uuid4())
        i = random.randint(100, 900)
        j = random.randint(100, 900)
        id = random.randint(1, 900)
        user = User(
            userID=id,
            phone=f"23490{j}00{i}",
            passwordHash="asdfjoasdfkl",
            metadata={}
        )
        v1 = self.db.createUser(user)
        assert type(v1) == UserInDB

        v2 = self.db.getUser(v1.userID)
        assert v2.phone == v1.phone

        v3 = self.db.updateUser(
            v1.userID, "metadata", json.dumps({"dob": "11-24-2001"})
        )
        assert v3.metadata == {"dob": "11-24-2001"}

        self.db.deleteUser(v1.userID)
        v4 = self.db.getUser(v1.userID)
        assert type(v4) == type(None)


class ContractTest(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.db = ContractDB("DeepaTest")

    def testContractCRUD(self):
        unq = str(uuid.uuid4())
        contract = Contract(
            contractID=str(uuid.uuid4()),
            contractTitle="Test Contract",
            contractDescription="A simple Contract",
            buyerID=2,
            productID=1,
        )
        v1 = self.db.createContract(contract)
        assert type(v1) == ContractInDB

        v2 = self.db.getContract(v1.contractID)
        assert v2.contractTitle == v1.contractTitle

        v3 = self.db.updateContract(
            v1.contractID, "metadata", json.dumps({"witness": "Femi Mecho"})
        )
        assert v3.metadata == {"witness": "Femi Mecho"}

        self.db.deleteContract(v1.contractID)
        v4 = self.db.getContract(v1.contractID)
        assert type(v4) == type(None)

class PaymentTest(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.cdb = ContractDB("DeepaTest")
        self.db = PaymentDB("DeepaTest")

    def testPaymentCRUD(self):
        contract = Contract(
            contractID=str(uuid.uuid4()),
            contractTitle="Test Contract",
            contractDescription="A simple Contract",
            buyerID=2,
            productID=1,
        )
        v1 = self.cdb.createContract(contract)
        payment = Payment(
            paymentID=str(uuid.uuid4()),
            amount=200,
            contractID=v1.id,
            metadata={"type": "fund_with_card"}
        )

        v2 = self.db.createPayment(payment)
        v3 = self.cdb.getContract(v1.id)
        assert type(v2) == PaymentInDB
        assert v3.fulfillmentStatus == "partiallyFulfilled"

        contract = Contract(
            contractID=str(uuid.uuid4()),
            contractTitle="Test Contract",
            contractDescription="A simple Contract",
            buyerID=2,
            productID=1,
        )
        vo1 = self.cdb.createContract(contract)
        payment = Payment(
            paymentID=str(uuid.uuid4()),
            amount=10000,
            contractID=vo1.id,
            metadata={"type": "fund_with_card"}
        )

        self.db.createPayment(payment)
        vo3 = self.cdb.getContract(vo1.id)
        assert vo3.fulfillmentStatus == "fulfilled"

        v4 = self.db.getPayment(v2.paymentID)
        assert v4.contractID == v2.contractID

        v5 = self.db.updatePayment(
            v4.paymentID, "metadata", json.dumps({"cardName": "Femi Mecho"})
        )
        assert v5.metadata == {"cardName": "Femi Mecho"}

        self.db.deletePayment(v4.paymentID)
        v6 = self.db.getPayment(v4.paymentID)
        assert type(v6) == type(None)

    def testMultiplePayment(self):
        pcontract = Contract(
            contractID=str(uuid.uuid4()),
            contractTitle="Test Contract for Multiple Payment",
            contractDescription="A simple Contract",
            buyerID=2,
            productID=1,
        )
        pv1 = self.cdb.createContract(pcontract)
        ppayment = Payment(
            paymentID=str(uuid.uuid4()),
            amount=2000,
            contractID=pv1.id,
            metadata={"type": "fund_with_card"}
        )
        self.db.createPayment(ppayment)
        pv3 = self.cdb.getContract(pv1.id)
        assert pv3.fulfillmentStatus == "partiallyFulfilled"

        sppayment = Payment(
            paymentID=str(uuid.uuid4()),
            amount=8000,
            contractID=pv1.id,
            metadata={"type": "fund_with_card"}
        )
        self.db.createPayment(sppayment)
        pv3 = self.cdb.getContract(pv1.id)
        assert pv3.fulfillmentStatus == "fulfilled"

        pv4 = self.cdb.getPayments(pv3.id)
        assert len(pv4) == 2
