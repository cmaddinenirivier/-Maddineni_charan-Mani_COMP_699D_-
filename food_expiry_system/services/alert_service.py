from datetime import datetime
from models.alert import create_alert
from models.grocery_item import get_all_items
from services.ml_service import get_item_risk


def generate_expiry_alerts(household_id, threshold_days=3):
    items = get_all_items(household_id)
    today = datetime.today()

    for item in items:
        try:
            expiry_date = datetime.strptime(item['expiry_date'], "%Y-%m-%d")
            days_left = (expiry_date - today).days

            if days_left <= threshold_days:
                message = f"Item '{item['name']}' is expiring in {days_left} day(s). Use soon."
                create_alert(item['id'], message, "expiry")

        except:
            continue


def generate_ml_alerts(household_id):
    items = get_all_items(household_id)

    for item in items:
        try:
            result = get_item_risk(item)

            if result['label'] == "At Risk":
                reasons = ", ".join(result.get('reasons', []))
                message = f"Item '{item['name']}' is at risk. {reasons}"
                create_alert(item['id'], message, "ml_risk")

        except:
            continue


def generate_all_alerts(household_id):
    generate_expiry_alerts(household_id)
    generate_ml_alerts(household_id)


def get_daily_reminders(household_id):
    items = get_all_items(household_id)
    today = datetime.today()

    reminders = []

    for item in items:
        try:
            expiry_date = datetime.strptime(item['expiry_date'], "%Y-%m-%d")
            days_left = (expiry_date - today).days

            if days_left <= 2:
                reminders.append({
                    "item_id": item['id'],
                    "name": item['name'],
                    "message": f"Use '{item['name']}' within {days_left} day(s)"
                })

        except:
            continue

    return reminders