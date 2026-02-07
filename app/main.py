from fastapi import FastAPI

from app.api.webhook import router as webhook_router

app = FastAPI(title="Pet-Planner")
app.include_router(webhook_router, prefix="/webhook")


@app.get("/health")
def health():
    return {"status": "ok"}
