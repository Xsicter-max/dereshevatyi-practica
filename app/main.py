from fastapi import FastAPI
from app.database import engine, Base

# Импорт моделей — ОБЯЗАТЕЛЬНО до create_all
from app.users.models import User
from app.auth.models import AuthSession
from app.tasks.models import Task

from app.users.router import router as users_router
from app.auth.router import router as auth_router
from app.tasks.router import router as tasks_router

app = FastAPI(title="Task Manager API", version="1.0.0")

app.include_router(users_router)
app.include_router(auth_router)
app.include_router(tasks_router)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.get("/api/health", tags=["health"])
def health():
    return {"status": "ok"}