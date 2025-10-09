from fastmcp import FastMCP
import os
import sqlite3

# Define DB path and category JSON path
DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")
CATEGORY_JSON_PATH = os.path.join(os.path.dirname(__file__), "categories.json")

mcp = FastMCP("ExpenseTracker")

# Initialize database
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT default '',
                description TEXT default ''
            )
        ''')
        conn.commit()

init_db()

@mcp.tool
def add_expense(date: str, amount: float, category: str, subcategory: str = "", description: str = "") -> dict:
    """Add a new expense to the database."""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO expenses (date, amount, category, subcategory, description)
            VALUES (?, ?, ?, ?, ?)
        ''', (date, amount, category, subcategory, description))
        conn.commit()
    return {"status": "success", "id": cur.lastrowid}

@mcp.tool
def get_expenses(start_date: str, end_date: str) -> list:
    """Retrieve expenses within a date range."""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute('''
            SELECT * FROM expenses
            WHERE date BETWEEN ? AND ?
            ORDER BY date ASC
        ''', (start_date, end_date))
        rows = cur.fetchall()
        cols = [column[0] for column in cur.description]
    return [dict(zip(cols, row)) for row in rows]

@mcp.tool
# Summarize expenses by category within a date range and optional category filter
def summarize_expenses(start_date: str, end_date: str, category: str = None) -> list:
    """Summarize expenses by category within a date range and optional category filter."""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        query = ('''
                SELECT category, SUM(amount) as total
                FROM expenses
                WHERE date BETWEEN ? AND ?
            ''')
        params = [start_date, end_date]
        if category:
            query += ' AND category = ?'
            params.append(category)
        query += ' GROUP BY category ORDER BY total DESC'
        cur.execute(query, params)
        rows = cur.fetchall()
        cols = [column[0] for column in cur.description]
    return [dict(zip(cols, row)) for row in rows]

# Category JSON as resource
@mcp.resource("expense://categories", mime_type="application/json")
def load_categories() -> str:
    """Load categories from the JSON file."""
    with open(CATEGORY_JSON_PATH, 'r', encoding='utf-8') as f:
        return f.read()


if __name__ == "__main__":
    mcp.run()