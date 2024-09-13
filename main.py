from datetime import datetime, timedelta, timezone
import json
import re
from typing import Annotated
import unicodedata
import uuid
import bcrypt
from typing import Any
from fastapi import Depends, FastAPI, HTTPException, status, Body
from pydantic import BaseModel
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from email_validator import EmailNotValidError, validate_email
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
import urllib
from thirdPartyIntegrations import fetchJumiaProduct
from models.store import Store
from models.product import Product
import database.product
import database.store
import database.user
from models.user import User, UserInDB
from passlib.context import CryptContext
from models.token import TokenData, Token
from fastapi.middleware.cors import CORSMiddleware
import database 


app = FastAPI(title="HallowPay")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["POST", "PUT", "OPTIONS", "GET"]
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30


class Manager(database.user.UserDB, database.store.StoreDB, database.product.ProductDB):
    """ """
    pass

manager = Manager()
manager.initializeSchema()

class DeepaJsonResponse:
    """ """

    def __init__(self, obj, *args, **kwargs) -> None:
        self.json = None

        response = obj(*args)
        self.json = {
            "message": response,
            "status": "00"
        }

    def unpack(self):
        """ """
        return self.json


def verify_password(plain_password, hashed_password):
    """

    :param plain_password: 
    :param hashed_password: 

    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """

    :param password: 

    """
    return pwd_context.hash(password)


def get_user(phone: str):
    """

    :param phone: str: 

    """
    u = manager.getUser(phone)
    if u:
        return u


def create_access_token(data: dict, expires_delta: timedelta = None):
    """

    :param data: dict: 
    :param expires_delta: timedelta:  (Default value = None)

    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(token_data.username)
    if user is None:
        raise credentials_exception
    return user

def url_path_join(*pieces):
    """

    :param *pieces: 

    """
    initial = pieces[0].startswith("/")
    final = pieces[-1].endswith("/")
    stripped = [s.strip("/") for s in pieces]
    result = "/".join(s for s in stripped if s)
    if initial:
        result = "/" + result
    if final:
        result = result + "/"
    if result == "//":
        result = "/"
    return result

def slugify(raw, base="", max_length=30):  # noqa
    """

    :param raw: 
    :param base:  (Default value = "")
    :param max_length:  (Default value = 30)

    """
    raw = raw if raw.startswith("/") else "/" + raw
    signature = ""
    base = (base if base.startswith("/") else "/" + base).lower()
    raw = raw.lower()
    common = 0
    limit = min(len(base), len(raw))
    while common < limit and base[common] == raw[common]:
        common += 1
    value = url_path_join(base[common:], raw)
    value = urllib.parse.unquote(value)
    value = unicodedata.normalize("NFKC", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^\w\s-]", "", value).strip()
    value = re.sub(r"[-\s]+", "-", value)
    return value[: max_length - len(signature)] + signature


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user


def authenticate_user(username: str, password: str):
    """

    :param username: str: 
    :param password: str: 

    """
    user = get_user(username)
    if not user:
        return None
    if not verify_password(password, user.passwordHash):
        return None
    return user


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    if exc.status_code == 401:

        def msg(e):
            """

            :param e: 

            """
            return "Authentication missing in request header or Invalid Authentication, Visit https://docs.trydeepa.com/authentication for help."

        result = DeepaJsonResponse(msg, 0)
        return JSONResponse(result.unpack(), status_code=exc.status_code)
    return JSONResponse(str(exc.detail), status_code=exc.status_code)


@app.get("/", response_class=JSONResponse)
def index(token: Annotated[str, Depends(oauth2_scheme)]):
    """

    :param token: Annotated[str: 
    :param Depends(oauth2_scheme)]: 

    """
    return {"api-version": 1.0, "version-name": "genesis", "status": "okay"}


@app.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    access_token = create_access_token(
        data={"sub": user.phone}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@app.post("/signup", response_class=JSONResponse)
def signup(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """

    :param form_data: Annotated[OAuth2PasswordRequestForm: 
    :param Depends()]: 

    """
    userID = uuid.uuid4()
    ashiri = get_password_hash(form_data.password)
    result = DeepaJsonResponse(
        manager.createUser, User(userID=str(userID), phone=form_data.username, passwordHash=ashiri, metadata={}), status="00"
    )
    return result.unpack()

@app.get("/store/{storeID}/revenue", response_class=JSONResponse)
def getTotalRevenue(current_user: Annotated[User, Depends(get_current_user)], storeID):
    """

    :param current_user: Annotated[User: 
    :param Depends(get_current_user)]: 
    :param storeID: 

    """
    result = DeepaJsonResponse(
        manager.getStoreRevenue, storeID, current_user.id, status="00"
    )
    return result.unpack()

@app.get("/store/{handle}", response_class=JSONResponse)
def getTotalRevenue(handle):
    """

    :param handle: 

    """
    result = DeepaJsonResponse(
        manager.getStore, handle, status="00"
    )
    return result.unpack()

@app.get("/product/{id}", response_class=JSONResponse)
def getProduct(id):
    """

    :param id: 

    """
    result = DeepaJsonResponse(
        manager.getProduct, id, status="00"
    )
    return result.unpack()

@app.get("/store/{storeID}/sales", response_class=JSONResponse)
def getSales(current_user: Annotated[User, Depends(get_current_user)], storeID):
    """

    :param current_user: Annotated[User: 
    :param Depends(get_current_user)]: 
    :param storeID: 

    """
    result = DeepaJsonResponse(
        manager.getStoreSales, storeID, current_user.id, status="00"
    )
    return result.unpack()

@app.get("/store/{storeID}/products", response_class=JSONResponse)
def getProducts(storeID):
    """

    :param storeID: 

    """
    result = DeepaJsonResponse(
        manager.getStoreProducts, storeID, status="00"
    )
    return result.unpack()


@app.get("/user/store/{storeID}/products", response_class=JSONResponse)
def getProducts(current_user: Annotated[User, Depends(get_current_user)], storeID):
    """

    :param current_user: Annotated[User: 
    :param Depends(get_current_user)]: 
    :param storeID: 

    """
    result = DeepaJsonResponse(
        manager.getStoreProducts, storeID, current_user.id, status="00"
    )
    return result.unpack()

@app.get("/user/store/{storeID}", response_class=JSONResponse)
def getProducts(current_user: Annotated[User, Depends(get_current_user)], storeID):
    """

    :param current_user: Annotated[User: 
    :param Depends(get_current_user)]: 
    :param storeID: 

    """
    result = DeepaJsonResponse(
        manager.getStore, storeID, current_user.id, status="00"
    )
    return result.unpack()

@app.get("/user/store/{storeID}/analytics", response_class=JSONResponse)
def getProducts(current_user: Annotated[User, Depends(get_current_user)], storeID):
    """

    :param current_user: Annotated[User: 
    :param Depends(get_current_user)]: 
    :param storeID: 

    """
    result = DeepaJsonResponse(
        manager.getStoreAnalytics, storeID, current_user.id, status="00"
    )
    return result.unpack()

@app.get("/user/store", response_class=JSONResponse)
def getStores(current_user: Annotated[User, Depends(get_current_user)]):
    """

    :param current_user: Annotated[User: 
    :param Depends(get_current_user)]: 

    """
    result = DeepaJsonResponse(
        manager.getStores, current_user.id, status="00"
    )
    return result.unpack()


class URL(BaseModel):
    """ """
    url: str
    storeID: str

@app.post("/product/create", response_class=JSONResponse)
def createProduct(current_user: Annotated[User, Depends(get_current_user)], product: Product):
    """

    :param current_user: Annotated[User: 
    :param Depends(get_current_user)]: 
    :param product: Product: 

    """
    product.userID = current_user.id
    product.productID = str(uuid.uuid4())
    product.storeID = manager.getStore(product.storeID, userID=current_user.id).storeID
    result = DeepaJsonResponse(
        manager.createProduct, product, status="00"
    )
    return result.unpack()


@app.post("/product/create/url", response_class=JSONResponse)
def createProductFromJumiaURL(current_user: Annotated[User, Depends(get_current_user)], url:URL):
    """

    :param current_user: Annotated[User: 
    :param Depends(get_current_user)]: 
    :param url:URL: 

    """
    res = fetchJumiaProduct(url.url)
    product = Product(**res)
    product.userID = current_user.id
    product.productID = str(uuid.uuid4())
    product.storeID = manager.getStore(url.storeID, userID=current_user.id).storeID
    result = DeepaJsonResponse(
        manager.createProduct, product, status="00"
    )
    return result.unpack()

@app.post("/store/create", response_class=JSONResponse)
def createProduct(current_user: Annotated[User, Depends(get_current_user)], store: Store):
    """

    :param current_user: Annotated[User: 
    :param Depends(get_current_user)]: 
    :param store: Store: 

    """
    store.userID = current_user.id
    store.storeID = str(uuid.uuid4())
    if store.handle == '':
        store.handle = slugify(store.storeTitle)
    result = DeepaJsonResponse(
        manager.createStore, store, status="00"
    )
    return result.unpack()

@app.post("/store/update", response_class=JSONResponse)
def createProduct(current_user: Annotated[User, Depends(get_current_user)], store: Store):
    """

    :param current_user: Annotated[User: 
    :param Depends(get_current_user)]: 
    :param store: Store: 

    """
    store.userID = current_user.id
    result = DeepaJsonResponse(
        manager.updateStoreBulk, store, status="00"
    )
    return result.unpack()

def dict_to_func(_dict):
    """

    :param _dict: 

    """
    return _dict

@app.get("/user/me", response_class=JSONResponse)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    result = DeepaJsonResponse(dict_to_func, current_user, status="00")
    return result.unpack()