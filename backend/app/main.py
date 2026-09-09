from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="СанычЪ API",
    version="0.1.0.1",
    lifespan=lifespan,
)


@app.get("/")
async def default():
    return {"Тестовая мейн страница"}


@app.get("/health")
async def health():
    return {"status": "ok"}