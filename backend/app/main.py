
from fastapi import FastAPI

from auth.router import router as auth_router

from missions.router import router as missions_router




app = FastAPI(
    title="СанычЪ API",
    version="0.1.0.1",

)


app.include_router(auth_router)
app.include_router(missions_router)


@app.get("/")
async def default():
    return {"Тестовая мейн страница"}


@app.get("/health")
async def health():
    return {"status": "ok"}