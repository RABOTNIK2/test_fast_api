from enum import Enum
from fastapi import Cookie, FastAPI, Body, Form, Response, UploadFile
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel, Field, HttpUrl, EmailStr
from typing import Annotated, Any
import datetime

app = FastAPI()

# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None


# class User(BaseModel):
#     username: str
#     full_name: str | None = None


# @app.put("/items/{item_id}")
# async def update_item(
#     item_id: int,
#     item: Item,
#     user: User,
#     importance: Annotated[int, Body(gt=0)],
#     q: str | None = None,
# ):
#     results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
#     if q:
#         results.update({"q": q})
#     return results

# class Image(BaseModel):
#     url: HttpUrl
#     name: str


# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float = Field(
#         gt = 0
#     )
#     tax: float = Field(
#         default=0, ge=0
#     )
#     tags: set[str] = set()
#     images: list[Image] | None = None


# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     results = {"item_id": item_id, "item": item}
#     return results

class TypeOfDeal(Enum):
    trade = "trade"
    nasledstvo = "nasledstvo"
    syd = "syd"

class Image(BaseModel):
    name: str
    url: HttpUrl

class User(BaseModel):
    username: str = Field(
        max_length=40, default="Гостяра ебанный"
    )
    password: str = Field(
        max_length=32, min_length=8
    )
    image: Image
    age: int | None = Field(
        default=None, ge=18, le=100
    )
    
class Deals(BaseModel):
    persons: list[User]
    type: TypeOfDeal
    date: datetime.date
    
@app.post("/deals")
async def create_deal(deal: Deals, success: Annotated[bool, Body()]):
    return {
        "Deal":deal,
        "Success": success
    }
    
@app.get("/items/")
async def read_items(ads_id: str | None = Cookie(default=None)):
    return {"ads_id": ads_id}

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    pass


class UserInDB(UserBase):
    hashed_password: str


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.model_dump(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved

@app.post("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}