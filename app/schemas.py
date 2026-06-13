from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date

class ExpenseCreate(BaseModel):
    amount: float = Field(gt=0)
    category_id: int
    description: Optional[str] = Field(default=None, max_length=100)
    date: date  

class ExpenseUpdate(BaseModel):
    amount: Optional[float]
    category: Optional[int] = None
    description: Optional[str] = Field(default=None, max_length=100)
    date: Optional[date]

class ExpenseOut(BaseModel):
    id: int
    amount: float
    category_id: int
    description: Optional[str]
    date: date
    created_at: datetime
    
class ExpenseDailySummary(BaseModel):
    date: date
    total_amount: float
    category_breakdown: dict[str, float]

class CategorySummary(BaseModel):
    amount: float
    percentage: float

class ExpenseMonthlySummary(BaseModel):
    month: str
    total_amount: float
    category_breakdown: dict[str, CategorySummary]
    highest_spending_category: str | None

class CategoryCreate(BaseModel):
    name: str = Field(min_length=3, max_length=50)

class CategoryOut(BaseModel):
    id: int
    name: str