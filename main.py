from datetime import datetime, timedelta, timezone
import json
import re
from typing import Annotated
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
from productFromJumia import fetch
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
    pass

manager = Manager()
manager.initializeSchema()

class DeepaJsonResponse:

    def __init__(self, obj, *args, **kwargs) -> None:
        self.json = None
        # try:
        response = obj(*args)
        self.json = {
            "message": response,
            "status": "00"
        }

        # except Exception as a:
        #     self.json = {
        #         "message": a.__str__(),
        #         "status": "11"
        #     }

    def unpack(self):
        return self.json


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(phone: str):
    u = manager.getUser(phone)
    if u:
        return u


def create_access_token(data: dict, expires_delta: timedelta = None):
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


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user


def authenticate_user(username: str, password: str):
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
            return "Authentication missing in request header or Invalid Authentication, Visit https://docs.trydeepa.com/authentication for help."

        result = DeepaJsonResponse(msg, 0)
        return JSONResponse(result.unpack(), status_code=exc.status_code)
    return JSONResponse(str(exc.detail), status_code=exc.status_code)


@app.get("/", response_class=JSONResponse)
def index(token: Annotated[str, Depends(oauth2_scheme)]):
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
    userID = uuid.uuid4()
    ashiri = get_password_hash(form_data.password)
    result = DeepaJsonResponse(
        manager.createUser, User(userID=str(userID), phone=form_data.username, passwordHash=ashiri, metadata={}), status="00"
    )
    return result.unpack()

@app.get("/store/{storeID}/revenue", response_class=JSONResponse)
def getTotalRevenue(current_user: Annotated[User, Depends(get_current_user)], storeID):
    result = DeepaJsonResponse(
        manager.getStoreRevenue, storeID, current_user.id, status="00"
    )
    return result.unpack()

@app.get("/store/{handle}", response_class=JSONResponse)
def getTotalRevenue(handle):
    result = DeepaJsonResponse(
        manager.getStore, handle, status="00"
    )
    return result.unpack()

@app.get("/product/{id}", response_class=JSONResponse)
def getProduct(id):
    result = DeepaJsonResponse(
        manager.getProduct, id, status="00"
    )
    return result.unpack()

@app.get("/store/{storeID}/sales", response_class=JSONResponse)
def getSales(current_user: Annotated[User, Depends(get_current_user)], storeID):
    result = DeepaJsonResponse(
        manager.getStoreSales, storeID, current_user.id, status="00"
    )
    return result.unpack()

@app.get("/store/{storeID}/products", response_class=JSONResponse)
def getProducts(storeID):
    result = DeepaJsonResponse(
        manager.getStoreProducts, storeID, status="00"
    )
    return result.unpack()


@app.get("/user/store/{storeID}/products", response_class=JSONResponse)
def getProducts(current_user: Annotated[User, Depends(get_current_user)], storeID):
    result = DeepaJsonResponse(
        manager.getStoreProducts, storeID, current_user.id, status="00"
    )
    return result.unpack()

@app.get("/user/store/{storeID}", response_class=JSONResponse)
def getProducts(current_user: Annotated[User, Depends(get_current_user)], storeID):
    result = DeepaJsonResponse(
        manager.getStore, storeID, current_user.id, status="00"
    )
    return result.unpack()

@app.get("/user/store/{storeID}/analytics", response_class=JSONResponse)
def getProducts(current_user: Annotated[User, Depends(get_current_user)], storeID):
    result = DeepaJsonResponse(
        manager.getStoreAnalytics, storeID, current_user.id, status="00"
    )
    return result.unpack()

@app.get("/user/store", response_class=JSONResponse)
def getStores(current_user: Annotated[User, Depends(get_current_user)]):
    result = DeepaJsonResponse(
        manager.getStores, current_user.id, status="00"
    )
    return result.unpack()


class URL(BaseModel):
    url: str
    storeID: str

@app.post("/product/create", response_class=JSONResponse)
def createProduct(current_user: Annotated[User, Depends(get_current_user)], product: Product):
    product.userID = current_user.id
    product.productID = str(uuid.uuid4())
    product.storeID = manager.getStore(product.storeID, userID=current_user.id).storeID
    result = DeepaJsonResponse(
        manager.createProduct, product, status="00"
    )
    return result.unpack()


@app.post("/product/create/url", response_class=JSONResponse)
def createProductFromJumiaURL(current_user: Annotated[User, Depends(get_current_user)], url:URL):
    res = fetch(url.url)
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
    store.userID = current_user.id
    store.storeID = str(uuid.uuid4())
    print(store)
    result = DeepaJsonResponse(
        manager.createStore, store, status="00"
    )
    return result.unpack()

def dict_to_func(_dict):
    return _dict

@app.get("/user/me", response_class=JSONResponse)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    result = DeepaJsonResponse(dict_to_func, current_user, status="00")
    return result.unpack()