from flask import Blueprint, render_template, redirect, session
from models.user import get_all_users
from services.ml_service import retrain_model
from utils.db import execute_query

admin_bp = Blueprint('admin', __name__)


def is_logged_in():
    return 'user_id' in session


def is_admin():
    return session.get('user_id') == 1


@admin_bp.route('/admin')
def admin_dashboard():
    if not is_logged_in():
        return redirect('/')

    if not is_admin():
        return redirect('/dashboard')

    users = get_all_users()

    query = "SELECT COUNT(*) as total FROM households"
    households = execute_query(query, fetch=True)

    query = "SELECT COUNT(*) as total FROM grocery_items"
    items = execute_query(query, fetch=True)

    return render_template(
        'admin.html',
        users=users,
        total_households=households[0]['total'] if households else 0,
        total_items=items[0]['total'] if items else 0
    )


@admin_bp.route('/admin/retrain')
def retrain():
    if not is_logged_in():
        return redirect('/')

    if not is_admin():
        return redirect('/dashboard')

    retrain_model()

    users = get_all_users()

    query = "SELECT COUNT(*) as total FROM households"
    households = execute_query(query, fetch=True)

    query = "SELECT COUNT(*) as total FROM grocery_items"
    items = execute_query(query, fetch=True)

    return render_template(
        'admin.html',
        users=users,
        total_households=households[0]['total'] if households else 0,
        total_items=items[0]['total'] if items else 0,
        message="Model retrained successfully"
    )