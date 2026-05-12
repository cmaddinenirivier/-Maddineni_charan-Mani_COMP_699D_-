from flask import Blueprint, render_template, request, redirect, session
from models.alert import get_active_alerts, mark_alert_as_read
from services.alert_service import generate_all_alerts, get_daily_reminders

alert_bp = Blueprint('alert', __name__)


def is_logged_in():
    return 'user_id' in session


@alert_bp.route('/alerts')
def alerts():
    if not is_logged_in():
        return redirect('/')

    household_id = request.args.get('household_id')

    if not household_id:
        return redirect('/households')

    household_id = int(household_id)

    alerts = get_active_alerts()
    reminders = get_daily_reminders(household_id)

    return render_template(
        'alerts.html',
        alerts=alerts,
        reminders=reminders,
        household_id=household_id
    )


@alert_bp.route('/alerts/generate')
def generate():
    if not is_logged_in():
        return redirect('/')

    household_id = request.args.get('household_id')

    if not household_id:
        return redirect('/households')

    household_id = int(household_id)

    generate_all_alerts(household_id)

    return redirect(f'/alerts?household_id={household_id}')


@alert_bp.route('/alerts/read/<int:alert_id>')
def mark_read(alert_id):
    if not is_logged_in():
        return redirect('/')

    household_id = request.args.get('household_id')

    mark_alert_as_read(alert_id)

    return redirect(f'/alerts?household_id={household_id}')