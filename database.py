import sqlite3

def create_database():
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            payer TEXT,
            card TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS savings_goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            current_amount REAL NOT NULL,
            target_amount REAL NOT NULL
        )
    """)    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recurring_expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            payer TEXT,
            card TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            budget REAL NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS monthly_budgets (
            month TEXT PRIMARY KEY,
            amount REAL NOT NULL
        )
    """)
    connection.commit()
    connection.close()


def add_expense(date, amount, category, description, payer, card):
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO expenses (date, amount, category, description, payer, card)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (date, amount, category, description, payer, card))

    connection.commit()
    connection.close()


def get_expenses():
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, date, category, amount, description, payer, card
        FROM expenses
        ORDER BY date DESC, id DESC
    """)

    expenses = cursor.fetchall()

    connection.close()

    return expenses

def delete_expense(expense_id):
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM expenses
        WHERE id = ?
    """, (expense_id,))

    connection.commit()
    connection.close()

def get_savings_goals():
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, current_amount, target_amount
        FROM savings_goals
    """)

    goals = cursor.fetchall()

    connection.close()

    return goals

def add_savings_goal(name, current_amount, target_amount):
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO savings_goals (
            name,
            current_amount,
            target_amount
        )
        VALUES (?, ?, ?)
    """, (
        name,
        current_amount,
        target_amount
    ))

    connection.commit()
    connection.close()

def delete_savings_goal(goal_id):
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM savings_goals
        WHERE id = ?
    """, (goal_id,))

    connection.commit()
    connection.close()    

def update_savings_goal_amount(goal_id, new_amount):
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE savings_goals
        SET current_amount = ?
        WHERE id = ?
    """, (new_amount, goal_id))

    connection.commit()
    connection.close()

def update_expense(expense_id, date, amount, category, description, payer, card):
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE expenses
        SET date = ?,
            amount = ?,
            category = ?,
            description = ?,
            payer = ?,
            card = ?
        WHERE id = ?
    """, (
        date,
        amount,
        category,
        description,
        payer,
        card,
        expense_id
    ))

    connection.commit()
    connection.close()

def add_recurring_expense(name, amount, category, description, payer, card):
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO recurring_expenses (
            name,
            amount,
            category,
            description,
            payer,
            card
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, amount, category, description, payer, card))

    connection.commit()
    connection.close()


def get_recurring_expenses():
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, amount, category, description, payer, card
        FROM recurring_expenses
    """)

    recurring_expenses = cursor.fetchall()

    connection.close()

    return recurring_expenses

def add_or_update_category(name, budget):
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO categories (name, budget)
        VALUES (?, ?)
        ON CONFLICT(name) DO UPDATE SET budget = excluded.budget
    """, (name, budget))

    connection.commit()
    connection.close()


def get_categories():
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT name, budget
        FROM categories
        ORDER BY name
    """)

    categories = cursor.fetchall()

    connection.close()

    return categories

def delete_category(name):
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM categories
        WHERE name = ?
    """, (name,))

    connection.commit()
    connection.close()

def delete_recurring_expense(recurring_id):
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM recurring_expenses
        WHERE id = ?
    """, (recurring_id,))

    connection.commit()
    connection.close()

def set_monthly_budget(month, amount):
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO monthly_budgets
        (month, amount)
        VALUES (?, ?)
    """, (month, amount))

    connection.commit()
    connection.close()

def get_monthly_budget(month):
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT amount
        FROM monthly_budgets
        WHERE month = ?
    """, (month,))

    result = cursor.fetchone()

    connection.close()

    if result:
        return result[0]

    return None

def update_recurring_expense(recurring_id, name, amount, category, description, payer, card):
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE recurring_expenses
        SET name = ?,
            amount = ?,
            category = ?,
            description = ?,
            payer = ?,
            card = ?
        WHERE id = ?
    """, (
        name,
        amount,
        category,
        description,
        payer,
        card,
        recurring_id
    ))

    connection.commit()
    connection.close()