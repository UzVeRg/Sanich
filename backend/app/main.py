from fastapi import FastAPI
# uvicorn app.main:app --reload
app = FastAPI(
    title="СанычЪ API",
    version="0.1.0",
)
print("Запущено")

@app.get("/health")
async def health():
    return {"status": "ok"}