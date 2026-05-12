from utils.db import execute_query, execute_one


def create_user(name, email, password):
    try:
        query = """
        INSERT INTO users (name, email, password)
        VALUES (?, ?, ?)
        """
        execute_query(query, (name, email, password), commit=True)
        return True
    except:
        return False


def get_user_by_email(email):
    query = "SELECT * FROM users WHERE email = ?"
    return execute_one(query, (email,))


def get_user_by_id(user_id):
    query = "SELECT * FROM users WHERE id = ?"
    return execute_one(query, (user_id,))


def validate_user(email, password):
    query = """
    SELECT * FROM users 
    WHERE email = ? AND password = ?
    """
    return execute_one(query, (email, password))


def update_user_profile(user_id, name, email):
    query = """
    UPDATE users
    SET name = ?, email = ?
    WHERE id = ?
    """
    execute_query(query, (name, email, user_id), commit=True)


def update_user_password(user_id, new_password):
    query = """
    UPDATE users
    SET password = ?
    WHERE id = ?
    """
    execute_query(query, (new_password, user_id), commit=True)


def delete_user(user_id):
    query = "DELETE FROM users WHERE id = ?"
    execute_query(query, (user_id,), commit=True)


def get_all_users():
    query = "SELECT * FROM users"
    return execute_query(query, fetch=True)