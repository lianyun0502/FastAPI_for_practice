'''
屬於 "main" 專案的路由器
'''

from fastapi import APIRouter
from typing import Union
from enum import Enum
from schemas import main_schemas

router = APIRouter()

@router.get("/", tags=['主頁'])
async def root():
    return {"message": "Hello World"}

# @app.get("/items/{item_id}")
# async def read_item(item_id: str, q: Union[str, None] = None, short: bool = False):
#     item = {"item_id": item_id}
#     if q:
#         item.update({"q": q})
#     if not short:
#         item.update(
#             {"description": "This is an amazing item that has a long description"}
#         )
#     return item


@router.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@router.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

@router.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Union[str, None] = None, short: bool = False
):
    '''
    多個路徑和查詢參數
    '''
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item
@router.get("/models/{model_name}")
async def get_model(model_name: main_schemas.ModelName):
    if model_name is main_schemas.ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@router.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@router.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


@router.put("/items/{item_id}")
async def create_item(item_id: int, item: main_schemas.Item, q: Union[str, None] = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result