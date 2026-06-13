from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date, datetime

class Category(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)

class Expense(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    amount: float = Field(gt=0)
    category_id: int = Field(foreign_key="category.id")
    description: Optional[str] = Field(default=None, max_length=100)
    date: date
    created_at: datetime = Field(default_factory=datetime.now)