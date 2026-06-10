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

@router.put("/{expense_id}", response_model=ExpenseOut)
def update_expense(expense_id: int, payload:ExpenseUpdate):
    """Update an expense by ID."""
    data = expenses
    for index, expense in enumerate(data):
        if expense['id'] == expense_id:
            update_expense = expense
            if payload.amount is not None:
                update_expense['amount'] = payload.amount
            if payload.catergory is not None:
                update_expense['category'] = payload.catergory
            if payload.description is not None:
                update_expense['description'] = payload.description
            if payload.date is not None:
                update_expense['date'] = payload.date
            data[index] = update_expense
            return update_expense
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@router.delete("/{expense_id}", response_model=ExpenseOut)
def delete_expense(expense_id: int):
    """Retrieve specific expense by ID."""
    data = expenses
    for index, expense in enumerate(data):
        if expense['id'] == expense_id:
            data.pop(index)
            return expense
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@router.get("/category/{category}", response_model=list[ExpenseOut])
def get_by_category(category: str):
    """Retrieve expenses by Caterogry."""
    data = expenses
    category_expenses = []
    for index, expense in enumerate(data):
        if expense['category'] == category:
            category_expenses.append(data[index])
    if len(category_expenses) > 0:
        return category_expenses
    return category_expenses
