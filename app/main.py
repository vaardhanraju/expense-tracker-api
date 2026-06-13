from fastapi import FastAPI
from app.db.database import create_db_and_tables
from app.routes.expenses import router as expenses_router

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(expenses_router)