from utils.db import execute_query, execute_one


def create_alert(item_id, message, alert_type):
    query = """
    INSERT INTO alerts (item_id, message, alert_type)
    VALUES (?, ?, ?)
    """
    execute_query(query, (item_id, message, alert_type), commit=True)


def get_alert_by_id(alert_id):
    query = "SELECT * FROM alerts WHERE id = ?"
    return execute_one(query, (alert_id,))


def get_all_alerts():
    query = """
    SELECT a.*, g.name as item_name
    FROM alerts a
    JOIN grocery_items g ON a.item_id = g.id
    ORDER BY a.created_at DESC
    """
    return execute_query(query, fetch=True)


def get_active_alerts():
    query = """
    SELECT a.*, g.name as item_name
    FROM alerts a
    JOIN grocery_items g ON a.item_id = g.id
    WHERE a.status = 'active'
    ORDER BY a.created_at DESC
    """
    return execute_query(query, fetch=True)


def get_alerts_by_item(item_id):
    query = """
    SELECT * FROM alerts
    WHERE item_id = ?
    ORDER BY created_at DESC
    """
    return execute_query(query, (item_id,), fetch=True)


def mark_alert_as_read(alert_id):
    query = """
    UPDATE alerts
    SET status = 'read'
    WHERE id = ?
    """
    execute_query(query, (alert_id,), commit=True)


def deactivate_alert(alert_id):
    query = """
    UPDATE alerts
    SET status = 'inactive'
    WHERE id = ?
    """
    execute_query(query, (alert_id,), commit=True)


def delete_alert(alert_id):
    query = "DELETE FROM alerts WHERE id = ?"
    execute_query(query, (alert_id,), commit=True)


def delete_alerts_by_item(item_id):
    query = "DELETE FROM alerts WHERE item_id = ?"
    execute_query(query, (item_id,), commit=True)