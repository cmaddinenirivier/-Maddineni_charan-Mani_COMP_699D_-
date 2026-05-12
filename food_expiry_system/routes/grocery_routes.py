
from flask import Blueprint, render_template, request, redirect, session
from models.grocery_item import (
    add_grocery_item,
    get_all_items,
    delete_grocery_item,
    update_grocery_item,
    record_usage,
    get_item_by_id
)

grocery_bp = Blueprint('grocery', __name__)


def is_logged_in():
    return 'user_id' in session


@grocery_bp.route('/items')
def items():
    if not is_logged_in():
        return redirect('/')

    household_id = request.args.get('household_id')

    if not household_id:
        return redirect('/households')

    household_id = int(household_id)
    items = get_all_items(household_id)

    return render_template('items.html', items=items, household_id=household_id)


@grocery_bp.route('/add_item', methods=['POST'])
def add_item():
    if not is_logged_in():
        return redirect('/')

    name = request.form.get('name')
    category = request.form.get('category')
    quantity = request.form.get('quantity')
    purchase_date = request.form.get('purchase_date')
    expiry_date = request.form.get('expiry_date')
    household_id = request.form.get('household_id')

    if not household_id:
        return redirect('/households')

    household_id = int(household_id)

    add_grocery_item(
        name,
        category,
        int(quantity),
        purchase_date,
        expiry_date,
        household_id
    )

    return redirect(f'/items?household_id={household_id}')


@grocery_bp.route('/delete_item/<int:item_id>')
def delete_item(item_id):
    if not is_logged_in():
        return redirect('/')

    household_id = request.args.get('household_id')

    delete_grocery_item(item_id)

    return redirect(f'/items?household_id={household_id}')


@grocery_bp.route('/update_item/<int:item_id>', methods=['POST'])
def update_item(item_id):
    if not is_logged_in():
        return redirect('/')

    name = request.form.get('name')
    category = request.form.get('category')
    quantity = request.form.get('quantity')
    purchase_date = request.form.get('purchase_date')
    expiry_date = request.form.get('expiry_date')
    household_id = request.form.get('household_id')

    update_grocery_item(
        item_id,
        name,
        category,
        int(quantity),
        purchase_date,
        expiry_date
    )

    return redirect(f'/items?household_id={household_id}')


@grocery_bp.route('/use_item/<int:item_id>', methods=['POST'])
def use_item(item_id):
    if not is_logged_in():
        return redirect('/')

    action = request.form.get('action')  # used / partial / wasted
    quantity = request.form.get('quantity')
    household_id = request.form.get('household_id')

    record_usage(item_id, action, int(quantity))

    return redirect(f'/items?household_id={household_id}')


@grocery_bp.route('/item/<int:item_id>')
def view_item(item_id):
    if not is_logged_in():
        return redirect('/')

    item = get_item_by_id(item_id)

    return render_template('item_detail.html', item=item)