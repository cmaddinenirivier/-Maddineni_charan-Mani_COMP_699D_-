from flask import Blueprint, render_template, request, redirect, session
from models.household import (
    create_household,
    get_user_households,
    add_member,
    remove_member,
    get_household_members,
    get_household_by_id
)

household_bp = Blueprint('household', __name__)


def is_logged_in():
    return 'user_id' in session


@household_bp.route('/households')
def households():
    if not is_logged_in():
        return redirect('/')

    user_id = session.get('user_id')
    households = get_user_households(user_id)

    return render_template('households.html', households=households)


@household_bp.route('/household/create', methods=['POST'])
def create():
    if not is_logged_in():
        return redirect('/')

    user_id = session.get('user_id')
    name = request.form.get('name')

    if not name:
        return redirect('/households')

    create_household(name, user_id)

    return redirect('/households')


@household_bp.route('/household/<int:household_id>')
def view_household(household_id):
    if not is_logged_in():
        return redirect('/')

    household = get_household_by_id(household_id)
    members = get_household_members(household_id)

    return render_template(
        'household_detail.html',
        household=household,
        members=members
    )


@household_bp.route('/household/<int:household_id>/add_member', methods=['POST'])
def add_member_route(household_id):
    if not is_logged_in():
        return redirect('/')

    user_id = request.form.get('user_id')

    if user_id:
        add_member(household_id, int(user_id))

    return redirect(f'/household/{household_id}')


@household_bp.route('/household/<int:household_id>/remove_member/<int:user_id>')
def remove_member_route(household_id, user_id):
    if not is_logged_in():
        return redirect('/')

    remove_member(household_id, user_id)

    return redirect(f'/household/{household_id}')