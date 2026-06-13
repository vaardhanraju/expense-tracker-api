from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select
from app.schemas import ExpenseCreate, ExpenseOut, ExpenseUpdate, ExpenseDailySummary, ExpenseMonthlySummary, CategoryOut, CategoryCreate
from datetime import datetime, date
from app.db.database import SessionDep
from app.db.models import Category, Expense
from typing import Annotated

router = APIRouter(prefix="/expenses", tags=["expenses"])

@router.get("/", response_model=list[ExpenseOut])
def get_expenses(
    session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100
):
    """Retrive all expenses."""
    expenses = session.exec(select(Expense).offset(offset).limit(limit)).all()
    return expenses


@router.post("/", response_model=ExpenseOut)
def create_expense(payload: ExpenseCreate, session: SessionDep):
    """Create an expense."""
    category = session.get(Category, payload.category_id)

    if not category:
         raise HTTPException(status_code=404, detail="Category not found")
    
    expense_db = Expense(
        amount=payload.amount,
        category_id=payload.category_id,
        description=payload.description,
        date=payload.date
    )
    session.add(expense_db)
    session.commit()
    session.refresh(expense_db)
    return expense_db


@router.post("/bulk", response_model=list[ExpenseOut])
def create_expenses(payload: list[ExpenseCreate]):
    """Create multiple expenses in a single request."""
    global next_id
    created_expenses = []

    for expense in payload:
        new_expense = {
            "id": next_id,
            "amount": expense.amount,
            "category": expense.category,
            "description": expense.description,
            "date": expense.date,
            "created_at": datetime.now()
        }

        next_id += 1
        expenses.append(new_expense)
        created_expenses.append(new_expense)

    return created_expenses


@router.get("/range", response_model=list[ExpenseOut])
def get_expense_range(start: str, end: str, session: SessionDep):
    start_date = date.fromisoformat(start)
    end_date = date.fromisoformat(end)
    range_expenses = session.exec(select(Expense).where(Expense.date.between(start_date, end_date)))

    return range_expenses


@router.get("/category/{category_name}", response_model=list[ExpenseOut])
def get_by_category(category_name: str, session: SessionDep):
    """Retrieve expenses by Caterogry."""
    category = session.exec(select(Category).where(Category.name == category_name)).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    
    category_expenses = session.exec(select(Expense).where(Expense.category_id == category.id)).all()
    return category_expenses


@router.get("/summary/day", response_model=ExpenseDailySummary)
def get_summary_by_day(date: date):
    """Retrieve summary by Day."""
    data = expenses
    total_spent = 0
    category_breakdown = {}

    for expense in data:
        if expense['date'] != date:
            continue

        amount = expense['amount']
        category = expense['category']

        total_spent += amount
        category_breakdown[expense['category']] = (
            category_breakdown.get(category, 0) + amount
        )

    return ExpenseDailySummary(
        date=date,
        total_amount=total_spent,
        category_breakdown=category_breakdown
    )


@router.get("/summary/month", response_model=ExpenseMonthlySummary)
def get_summary_by_month(date: str):
    """Retrieve summary by Day."""
    data = expenses
    total_spent = 0
    category_spent = {}
    category_breakdown = {}
    highest_spent_amount = 0
    highest_spending_category = None

    for expense in data:
        date_str_converted = str(expense['date'])
        if date == date_str_converted[:7]:

            amount = expense['amount']
            category = expense['category']

            total_spent += amount
            category_spent[expense['category']] = (
                category_spent.get(category, 0) + amount
            )

    if total_spent == 0:
        return ExpenseMonthlySummary(
            month=date,
            total_amount=0,
            category_breakdown={},
            highest_spending_category=None
        )

    for category, amt in category_spent.items():
        category_breakdown[category] = {
            "amount": amt,
            "percentage": f"{(amt/total_spent) * 100:.2f}"
        }
        if amt > highest_spent_amount:
            highest_spent_amount = amt
            highest_spending_category = category

    return ExpenseMonthlySummary(
        month=date,
        total_amount=total_spent,
        category_breakdown=category_breakdown,
        highest_spending_category=highest_spending_category
    )


@router.get("/{expense_id}", response_model=ExpenseOut)
def get_expense(expense_id: int, session: SessionDep):
    """Retrieve specific expense by ID."""
    expense_db = session.get(Expense, expense_id)
    if not expense_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID not found")
    
    return expense_db


@router.put("/{expense_id}", response_model=ExpenseOut)
def update_expense(expense_id: int, payload: ExpenseUpdate, session: SessionDep):
    """Update an expense by ID."""
    expense_db = session.get(Expense, expense_id)
    if not expense_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID not found")
    
    expense_data = payload.model_dump(exclude_unset=True)
    expense_db.sqlmodel_update(expense_data)
    session.add(expense_db)
    session.commit()
    session.refresh(expense_db)
    return expense_db


@router.delete("/{expense_id}")
def delete_expense(expense_id: int, session: SessionDep):
    """Delete specific expense by ID."""
    expense = session.get(Expense, expense_id)
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID not found")
    session.delete(expense)
    session.commit()
    return {"ok": True}


@router.post("/categories", response_model=CategoryOut)
def create_category(category: CategoryCreate, session:SessionDep):
    existing = session.exec(select(Category).where(Category.name == category.name)).first()
    if existing:
        return existing
    db_category = Category(name = category.name)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category
