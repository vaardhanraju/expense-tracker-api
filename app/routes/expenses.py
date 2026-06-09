from fastapi import APIRouter, HTTPException, status
from app.schemas import ExpenseCreate, ExpenseOut, ExpenseUpdate

router = APIRouter(prefix="/expenses", tags=["expenses"])

next_id = 1

expenses = []

@router.get("/", response_model=list[ExpenseOut])
def get_expenses():
    "Retrive all expenses."
    data = expenses
    return data
