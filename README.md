# Expense Tracker API

A FastAPI-based REST API for tracking personal expenses with SQLite database, category management, and spending summaries.

## Features

- Create, read, update, and delete expenses
- Manage expense categories
- Bulk create expenses and categories
- Filter expenses by category and date range
- Daily and monthly spending summaries with category breakdown
- Calculate highest spending category per month
- Pagination support

## Tech Stack

- **FastAPI** - Web framework
- **SQLModel** - ORM for database
- **SQLite** - Database
- **Pydantic** - Data validation
- **Python 3.9+**

## Setup

### Installation

```bash
git clone https://github.com/yourusername/expense-tracker-api.git
cd expense-tracker-api
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Running

```bash
uvicorn app.main:app --reload
```

Visit `http://localhost:8000/docs` for interactive API documentation.

## API Endpoints

### Categories
- `POST /expenses/categories` - Create category
- `POST /expenses/categories/bulk` - Create multiple categories

### Expenses
- `POST /expenses` - Create expense
- `GET /expenses` - Get all expenses (with pagination)
- `GET /expenses/{id}` - Get expense by ID
- `PUT /expenses/{id}` - Update expense
- `DELETE /expenses/{id}` - Delete expense
- `POST /expenses/bulk` - Create multiple expenses

### Filters & Summaries
- `GET /expenses/category/{category_name}` - Get expenses by category
- `GET /expenses/range?start=YYYY-MM-DD&end=YYYY-MM-DD` - Get expenses by date range
- `GET /expenses/summary/day?date=YYYY-MM-DD` - Daily summary
- `GET /expenses/summary/month?date=YYYY-MM` - Monthly summary

## Database

SQLite database is created automatically at `database.db` when you first run the app.

## Project Structure

```
expense-tracker-api/
├── app/
│   ├── main.py
│   ├── schemas.py
│   ├── db/
│   │   ├── database.py
│   │   └── models.py
│   └── routes/
│       └── expenses.py
├── requirements.txt
└── README.md
```