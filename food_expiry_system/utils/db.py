import sqlite3
from config import DATABASE


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS households (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        owner_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS household_members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        household_id INTEGER,
        user_id INTEGER,
        role TEXT DEFAULT 'member'
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS grocery_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT,
        quantity INTEGER,
        purchase_date TEXT,
        expiry_date TEXT,
        status TEXT DEFAULT 'active',
        household_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS item_usage (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id INTEGER,
        action TEXT,
        quantity INTEGER,
        action_date TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id INTEGER,
        message TEXT,
        alert_type TEXT,
        status TEXT DEFAULT 'active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ml_training_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id INTEGER,
        days_since_purchase INTEGER,
        days_to_expiry INTEGER,
        category TEXT,
        usage_frequency REAL,
        label INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def execute_query(query, params=(), fetch=False, commit=False):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(query, params)

    data = None

    if fetch:
        data = cursor.fetchall()

    if commit:
        conn.commit()

    conn.close()
    return data


def execute_one(query, params=()):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(query, params)
    data = cursor.fetchone()
    conn.close()
    return data