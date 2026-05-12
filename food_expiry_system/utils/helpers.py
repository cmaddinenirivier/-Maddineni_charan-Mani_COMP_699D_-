from datetime import datetime


def calculate_days_to_expiry(expiry_date):
    try:
        today = datetime.today()
        expiry = datetime.strptime(expiry_date, "%Y-%m-%d")
        return (expiry - today).days
    except:
        return 0


def calculate_days_since_purchase(purchase_date):
    try:
        today = datetime.today()
        purchase = datetime.strptime(purchase_date, "%Y-%m-%d")
        return (today - purchase).days
    except:
        return 0


def format_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%d-%m-%Y")
    except:
        return date_str


def safe_int(value, default=0):
    try:
        return int(value)
    except:
        return default


def safe_float(value, default=0.0):
    try:
        return float(value)
    except:
        return default