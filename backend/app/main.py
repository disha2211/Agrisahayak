from fastapi import FastAPI

app = FastAPI(
    title="AgriSahayak AI",
    version="1.0.0",
    description="AI-powered multi-agent assistant for farmers."
)


@app.get("/")
async def root():
    return {
        "message": "Welcome to AgriSahayak AI 🚜"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }