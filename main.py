
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

expenses = {}
next_id = 1


class Expense(BaseModel):
    description: str
    amount: float = Field(gt=0)
    category: str


@app.post("/expenses")
def add_expense(expense: Expense):
    global next_id

    if not expense.description.strip():
        raise HTTPException(400, "Description cannot be empty")

    if not expense.category.strip():
        raise HTTPException(400, "Category cannot be empty")

    expense_id = next_id
    next_id += 1

    expenses[expense_id] = {
        "id": expense_id,
        "description": expense.description.strip(),
        "amount": expense.amount,
        "category": expense.category.strip()
    }

    return {
        "message": "Expense added successfully",
        "expense": expenses[expense_id]
    }


@app.get("/expenses")
def get_expenses():
    return list(expenses.values())


@app.put("/expenses/{expense_id}")
def update_expense(expense_id: int, expense: Expense):
    if expense_id not in expenses:
        raise HTTPException(404, "Expense not found")

    if not expense.description.strip():
        raise HTTPException(400, "Description cannot be empty")

    if not expense.category.strip():
        raise HTTPException(400, "Category cannot be empty")

    expenses[expense_id] = {
        "id": expense_id,
        "description": expense.description.strip(),
        "amount": expense.amount,
        "category": expense.category.strip()
    }

    return {
        "message": "Expense updated successfully",
        "expense": expenses[expense_id]
    }


@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):
    if expense_id not in expenses:
        raise HTTPException(404, "Expense not found")

    deleted = expenses.pop(expense_id)

    return {
        "message": "Expense deleted successfully",
        "expense": deleted
    }
