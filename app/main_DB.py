from sql_app import CURD
from sql_app import schemas
from sql_app import models
from sql_app.database import SessionLocal, engine

from fastapi import FastAPI, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import Annotated

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title='FastAPI DB 4 Pactice')

#Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close_all()

@app.get("/", response_class=HTMLResponse)
def read_root():
    with open('app\index.html', 'r', encoding='utf-8') as f:
        return f.read()

@app.post("/users/", response_model=schemas.User)
def create_user(user:schemas.UserCreate, db:Session=Depends(get_db)):
    db_user = CURD.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return CURD.create_user(db=db, user=user)

@app.post("/users_form/")
def create_user_form(email:str=Form(), password:str=Form(),  db:Session=Depends(get_db), response_model=schemas.User):
    user = schemas.UserCreate(email=email, password=password)
    db_user = CURD.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return CURD.create_user(db=db, user=user)

@app.get("/users/", response_model=list[schemas.User])
def read_users(skip:int=0, limit:int=100, db:Session=Depends(get_db)):
    users = CURD.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id:int, db:Session=Depends(get_db)):
    db_user = CURD.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user  

@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(user_id:int, item:schemas.ItemCreate, db:Session=Depends(get_db)):
    return CURD.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip:int=0, limit:int=100, db:Session=Depends(get_db)):
    items = CURD.get_items(db, skip=skip, limit=limit)
    return items


if __name__ == '__main__':
    import uvicorn
    from setting import settings
    uvicorn.run('main_DB:app', host='127.0.0.1', port=settings.PORT, reload=settings.DEBUG)