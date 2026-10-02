from fastapi import FastAPI
from app.database import engine, Base

app = FastAPI(
    title="Restaurant API",
    description="Backend сервис для ресторана",
    version="0.1.0",
)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Restaurant API работает"}