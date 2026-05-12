from models.grocery_item import get_all_items
from utils.db import execute_query


def get_weekly_waste_trend(household_id):
    query = """
    SELECT strftime('%Y-%W', iu.action_date) AS week, COUNT(*) as waste_count
    FROM item_usage iu
    JOIN grocery_items gi ON iu.item_id = gi.id
    WHERE iu.action = 'wasted' AND gi.household_id = ?
    GROUP BY week
    ORDER BY week DESC
    """
    return execute_query(query, (household_id,), fetch=True)


def get_category_wise_waste(household_id):
    query = """
    SELECT gi.category, COUNT(*) as waste_count
    FROM item_usage iu
    JOIN grocery_items gi ON iu.item_id = gi.id
    WHERE iu.action = 'wasted' AND gi.household_id = ?
    GROUP BY gi.category
    ORDER BY waste_count DESC
    """
    return execute_query(query, (household_id,), fetch=True)


def get_total_items(household_id):
    query = """
    SELECT COUNT(*) as total
    FROM grocery_items
    WHERE household_id = ?
    """
    result = execute_query(query, (household_id,), fetch=True)
    return result[0]['total'] if result else 0


def get_wasted_items_count(household_id):
    query = """
    SELECT COUNT(*) as wasted
    FROM item_usage iu
    JOIN grocery_items gi ON iu.item_id = gi.id
    WHERE iu.action = 'wasted' AND gi.household_id = ?
    """
    result = execute_query(query, (household_id,), fetch=True)
    return result[0]['wasted'] if result else 0


def get_used_items_count(household_id):
    query = """
    SELECT COUNT(*) as used
    FROM item_usage iu
    JOIN grocery_items gi ON iu.item_id = gi.id
    WHERE iu.action = 'used' AND gi.household_id = ?
    """
    result = execute_query(query, (household_id,), fetch=True)
    return result[0]['used'] if result else 0


def get_expiring_soon_count(household_id, threshold_days=3):
    items = get_all_items(household_id)
    from datetime import datetime

    today = datetime.today()
    count = 0

    for item in items:
        try:
            expiry_date = datetime.strptime(item['expiry_date'], "%Y-%m-%d")
            days_left = (expiry_date - today).days

            if days_left <= threshold_days:
                count += 1
        except:
            continue

    return count


def get_dashboard_summary(household_id):
    return {
        "total_items": get_total_items(household_id),
        "used_items": get_used_items_count(household_id),
        "wasted_items": get_wasted_items_count(household_id),
        "expiring_soon": get_expiring_soon_count(household_id)
    }