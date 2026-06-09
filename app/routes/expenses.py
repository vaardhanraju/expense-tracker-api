from fastapi import APIRouter, HTTPException, status
from app.schemas import ExpenseCreate, ExpenseOut, ExpenseUpdate
from datetime import datetime

router = APIRouter(prefix="/expenses", tags=["expenses"])

next_id = 1

expenses = []

@router.get("/", response_model=list[ExpenseOut])
def get_expenses():
    """Retrive all expenses."""
    data = expenses
    return data

@router.get("/{expense_id}", response_model=ExpenseOut)
def get_expense(expense_id: int):
    """Retrieve specific expense by ID."""
    data = expenses
    for index, expense in enumerate(data):
        if expense['id'] == expense_id:
            return data[index]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@router.post("/", response_model=ExpenseOut)
def create_expense(payload: ExpenseCreate):
    """Create an expense."""
    global next_id
    new_expense = {
        "id": next_id,
        "amount": payload.amount,
        "category": payload.category,
        "description": payload.description,
        "date": payload.date,
        "created_at": datetime.now()
    }
    next_id += 1
    expenses.append(new_expense)
    return new_expense