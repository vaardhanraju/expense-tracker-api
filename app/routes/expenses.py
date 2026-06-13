from fastapi import APIRouter, HTTPException, status, Query
from sqlmodel import select
from sqlalchemy import func, extract
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
def create_expenses(payload: list[ExpenseCreate], session: SessionDep):
    """Create multiple expenses in a single request."""
    created_expenses = []

    try: 
        for expense_data in payload:
            category = session.get(Category, expense_data.category_id)
            if not category:
                raise HTTPException(status_code=404, detail=f"Category {expense_data.category_id} not found")
            
            db_expense = Expense(
                amount=expense_data.amount,
                category_id=expense_data.category_id,
                description=expense_data.description,
                date=expense_data.date
            )
            session.add(db_expense)
            created_expenses.append(db_expense)

        session.commit()
        
        for expense in created_expenses:
            session.refresh(expense)

        return created_expenses

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/range", response_model=list[ExpenseOut])
def get_expense_range(start: str, end: str, session: SessionDep):
    start_date = date.fromisoformat(start)
    end_date = date.fromisoformat(end)
    range_expenses = session.exec(select(Expense).where(Expense.date.between(start_date, end_date))).all()

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
def get_summary_by_day(date: date, session: SessionDep):
    """Retrieve summary by Day."""

    expenses = session.exec(select(Expense).where(Expense.date == date)).all()

    total_spent = sum(expense.amount for expense in expenses)
    category_breakdown = {}

    for expense in expenses:
        category = session.get(Category, expense.category_id)
        category_name = category.name
        category_breakdown[category_name] = category_breakdown.get(category_name, 0) + expense.amount

    return ExpenseDailySummary(
        date=date,
        total_amount=total_spent,
        category_breakdown=category_breakdown
    )


@router.get("/summary/month", response_model=ExpenseMonthlySummary)
def get_summary_by_month(date: str, session: SessionDep):
    """Retrieve summary by Day."""

    year, month = date.split('-') 
    expenses = session.exec(
        select(Expense).where(
            (extract('year', Expense.date) == int(year)) &
            (extract('month', Expense.date) == int(month))
        )
    ).all()

    total_spent = sum(expense.amount for expense in expenses)
    category_spent = {}
    category_breakdown = {}
    highest_spent_amount = 0
    highest_spending_category = None

    for expense in expenses:
        category = session.get(Category, expense.category_id)
        category_name = category.name
        category_spent[category_name] = category_spent.get(category_name, 0) + expense.amount

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

@router.post("/categories/bulk", response_model=list[CategoryOut])
def create_categories(payload: list[CategoryCreate], session: SessionDep):
    """Create multiple categories in a single request."""
    created_categories = []

    try:
        for category_data in payload:
            # Check if category already exists
            existing = session.exec(select(Category).where(Category.name == category_data.name)).first()
            
            if existing:
                created_categories.append(existing)
            else:
                # Create new category
                db_category = Category(name=category_data.name)
                session.add(db_category)
                created_categories.append(db_category)

        # Commit all at once
        session.commit()
        
        # Refresh all
        for category in created_categories:
            session.refresh(category)

        return created_categories
    
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))