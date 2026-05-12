from flask import Blueprint, render_template, request, redirect, session
from models.grocery_item import get_near_expiry_items
from services.analytics_service import get_dashboard_summary, get_weekly_waste_trend
from services.ml_service import get_item_risk

dashboard_bp = Blueprint('dashboard', __name__)


def is_logged_in():
    return 'user_id' in session


@dashboard_bp.route('/dashboard')
def dashboard():
    if not is_logged_in():
        return redirect('/')

    household_id = request.args.get('household_id')

    if not household_id:
        return redirect('/households')

    household_id = int(household_id)

    # Get near expiry items
    items = get_near_expiry_items(household_id)

    # Add ML prediction to each item
    enriched_items = []
    for item in items:
        item_dict = dict(item)
        risk = get_item_risk(item)
        item_dict['risk_label'] = risk.get('label')
        item_dict['risk_probability'] = risk.get('probability')
        item_dict['risk_reasons'] = ", ".join(risk.get('reasons', []))
        enriched_items.append(item_dict)

    # Dashboard analytics
    summary = get_dashboard_summary(household_id)
    trends = get_weekly_waste_trend(household_id)

    return render_template(
        'dashboard.html',
        items=enriched_items,
        summary=summary,
        trends=trends,
        household_id=household_id
    )