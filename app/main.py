from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv

from app.api.webhook import router as webhook_router
from app.services.reminders import send_due_reminders

load_dotenv()

app = FastAPI(title="Pet-Planner")
app.include_router(webhook_router, prefix="/webhook")

scheduler = BackgroundScheduler()


@app.on_event("startup")
def startup():
    scheduler.add_job(send_due_reminders, "interval", minutes=1)
    scheduler.start()


@app.on_event("shutdown")
def shutdown():
    scheduler.shutdown(wait=False)


@app.get("/health")
def health():
    return {"status": "ok"}
