# Expense Tracker API

A FastAPI-based REST API for tracking expenses with summaries and filtering.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Visit `http://localhost:8000/docs` for interactive API docs.

## Endpoints

- `POST /expenses` - Create expense
- `GET /expenses` - Get all expenses
- `GET /expenses/{id}` - Get expense by ID
- `PUT /expenses/{id}` - Update expense
- `DELETE /expenses/{id}` - Delete expense
- `POST /expenses/bulk` - Create multiple expenses
- `GET /expenses/category/{category}` - Filter by category
- `GET /expenses/range?start=DATE&end=DATE` - Filter by date range
- `GET /expenses/summary/day?date=DATE` - Daily summary
- `GET /expenses/summary/month?date=YYYY-MM` - Monthly summary

## Stack

FastAPI, Pydantic, Python 3.9+