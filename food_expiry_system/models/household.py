from utils.db import execute_query, execute_one


def create_household(name, owner_id):
    query = """
    INSERT INTO households (name, owner_id)
    VALUES (?, ?)
    """
    execute_query(query, (name, owner_id), commit=True)

    # get created household id
    household = execute_one(
        "SELECT * FROM households WHERE owner_id = ? ORDER BY id DESC LIMIT 1",
        (owner_id,)
    )

    # add owner as member
    add_member(household['id'], owner_id, role='owner')

    return household


def get_household_by_id(household_id):
    query = "SELECT * FROM households WHERE id = ?"
    return execute_one(query, (household_id,))


def get_user_households(user_id):
    query = """
    SELECT h.*
    FROM households h
    JOIN household_members hm ON h.id = hm.household_id
    WHERE hm.user_id = ?
    """
    return execute_query(query, (user_id,), fetch=True)


def add_member(household_id, user_id, role='member'):
    query = """
    INSERT INTO household_members (household_id, user_id, role)
    VALUES (?, ?, ?)
    """
    execute_query(query, (household_id, user_id, role), commit=True)


def remove_member(household_id, user_id):
    query = """
    DELETE FROM household_members
    WHERE household_id = ? AND user_id = ?
    """
    execute_query(query, (household_id, user_id), commit=True)


def get_household_members(household_id):
    query = """
    SELECT u.id, u.name, u.email, hm.role
    FROM users u
    JOIN household_members hm ON u.id = hm.user_id
    WHERE hm.household_id = ?
    """
    return execute_query(query, (household_id,), fetch=True)


def delete_household(household_id):
    # remove members first
    execute_query(
        "DELETE FROM household_members WHERE household_id = ?",
        (household_id,),
        commit=True
    )

    # remove grocery items linked to household
    execute_query(
        "DELETE FROM grocery_items WHERE household_id = ?",
        (household_id,),
        commit=True
    )

    # delete household
    execute_query(
        "DELETE FROM households WHERE id = ?",
        (household_id,),
        commit=True
    )


def get_household_owner(household_id):
    query = """
    SELECT u.*
    FROM users u
    JOIN households h ON u.id = h.owner_id
    WHERE h.id = ?
    """
    return execute_one(query, (household_id,))