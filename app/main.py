from fastapi import FastAPI
from app.routes.expenses import router as expenses_router
app = FastAPI()

app.include_router(expenses_router)