from fastapi import FastAPI
from routers import main_route


app = FastAPI(title='FastAPI 4 Pactice',
              description='FastAPI 4 Pactice',
              version='1.0.0',
              debug=True)

routers = (main_route.router,)

for router in routers:
    app.include_router(router)



if __name__ == '__main__':
    import uvicorn
    from setting import settings
    uvicorn.run('main:app', host='127.0.0.1', port=settings.PORT, reload=settings.DEBUG)