from fastapi import FastAPI
# uvicorn backend.app.main:app --reload
app = FastAPI(
    title="СанычЪ API",
    version="0.1.0.1",
)
@app.get("/")
async def default():
    return {"Тестовая мейн страница"}

@app.get("/health")
async def health():
    return {"status": "ok"}