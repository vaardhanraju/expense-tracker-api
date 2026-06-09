from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date

class ExpenseCreate(BaseModel):
    amount: float = Field(gt=0)
    category: str = Field(min_length=3, max_length=20)
    description: Optional[str] = Field(default=None, max_length=100)
    date: date  

class ExpenseUpdate(BaseModel):
    amount: Optional[float]
    catergory: Optional[str] = Field(min_length=3, max_length=20)
    description: Optional[str] = Field(default=None, max_length=100)
    date: Optional[datetime]

class ExpenseOut(BaseModel):
    id: int
    amount: float
    category: str
    description: str
    date: date
    created_at: datetime
    

