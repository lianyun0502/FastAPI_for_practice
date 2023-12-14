from fastapi import APIRouter, Header, Cookie, Response
from fastapi.responses import HTMLResponse, JSONResponse
from typing import Union, Annotated

router = APIRouter()


@router.get("/items/header/")
async def read_header_item(user_agent: Annotated[Union[str, None], Header()] = None):
    return {"User-Agent": user_agent}


@router.get("/items/cookie/")
async def read_cookie_item(ads_id: Annotated[Union[str, None], Cookie()] = None):
    content = {"message": "Come to the dark side, we have cookies", "ads_id": ads_id}
    response = JSONResponse(content=content)
    response.set_cookie(key="ads_id", value=ads_id)
    return response
