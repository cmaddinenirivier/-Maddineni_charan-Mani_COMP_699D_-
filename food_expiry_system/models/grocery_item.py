from utils.db import execute_query, execute_one
from datetime import datetime


def add_grocery_item(name, category, quantity, purchase_date, expiry_date, household_id):
    query = """
    INSERT INTO grocery_items (name, category, quantity, purchase_date, expiry_date, household_id)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    execute_query(query, (name, category, quantity, purchase_date, expiry_date, household_id), commit=True)


def get_item_by_id(item_id):
    query = "SELECT * FROM grocery_items WHERE id = ?"
    return execute_one(query, (item_id,))


def get_all_items(household_id):
    query = """
    SELECT * FROM grocery_items
    WHERE household_id = ?
    ORDER BY expiry_date ASC
    """
    return execute_query(query, (household_id,), fetch=True)


def update_grocery_item(item_id, name, category, quantity, purchase_date, expiry_date):
    query = """
    UPDATE grocery_items
    SET name = ?, category = ?, quantity = ?, purchase_date = ?, expiry_date = ?
    WHERE id = ?
    """
    execute_query(query, (name, category, quantity, purchase_date, expiry_date, item_id), commit=True)


def delete_grocery_item(item_id):
    query = "DELETE FROM grocery_items WHERE id = ?"
    execute_query(query, (item_id,), commit=True)


def update_item_status(item_id, status):
    query = """
    UPDATE grocery_items
    SET status = ?
    WHERE id = ?
    """
    execute_query(query, (status, item_id), commit=True)


def record_usage(item_id, action, quantity):
    action_date = datetime.now().strftime("%Y-%m-%d")

    query = """
    INSERT INTO item_usage (item_id, action, quantity, action_date)
    VALUES (?, ?, ?, ?)
    """
    execute_query(query, (item_id, action, quantity, action_date), commit=True)

    update_item_status(item_id, action)


def get_items_by_category(household_id, category):
    query = """
    SELECT * FROM grocery_items
    WHERE household_id = ? AND category = ?
    ORDER BY expiry_date ASC
    """
    return execute_query(query, (household_id, category), fetch=True)


def get_items_by_expiry_window(household_id, days):
    items = get_all_items(household_id)
    today = datetime.today()

    filtered = []

    for item in items:
        expiry_date = datetime.strptime(item['expiry_date'], "%Y-%m-%d")
        remaining = (expiry_date - today).days

        if remaining <= days:
            filtered.append(item)

    return filtered


def get_sorted_items(household_id):
    return get_all_items(household_id)


def get_near_expiry_items(household_id, threshold=3):
    return get_items_by_expiry_window(household_id, threshold)


def get_usage_history(item_id):
    query = """
    SELECT * FROM item_usage
    WHERE item_id = ?
    ORDER BY action_date DESC
    """
    return execute_query(query, (item_id,), fetch=True)


def get_weekly_waste_summary(household_id):
    query = """
    SELECT strftime('%Y-%W', action_date) AS week, COUNT(*) as waste_count
    FROM item_usage iu
    JOIN grocery_items gi ON iu.item_id = gi.id
    WHERE iu.action = 'wasted' AND gi.household_id = ?
    GROUP BY week
    ORDER BY week DESC
    """
    return execute_query(query, (household_id,), fetch=True)


def calculate_days_to_expiry(expiry_date):
    today = datetime.today()
    expiry = datetime.strptime(expiry_date, "%Y-%m-%d")
    return (expiry - today).days


def calculate_days_since_purchase(purchase_date):
    today = datetime.today()
    purchase = datetime.strptime(purchase_date, "%Y-%m-%d")
    return (today - purchase).days