import unittest
from services.ml_service import get_item_risk
from utils.db import init_db, get_connection


class TestMLModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        init_db()

        conn = get_connection()
        cursor = conn.cursor()

        # --------------------------
        # INSERT REQUIRED DATA FIRST
        # --------------------------

        # Insert user
        cursor.execute("""
        INSERT OR IGNORE INTO users (id, name, email, password_hash)
        VALUES (1, 'Test User', 'test@example.com', '123')
        """)

        # Insert household
        cursor.execute("""
        INSERT OR IGNORE INTO households (id, name, created_by)
        VALUES (1, 'Test Household', 1)
        """)

        # Insert membership
        cursor.execute("""
        INSERT OR IGNORE INTO household_members (user_id, household_id)
        VALUES (1, 1)
        """)

        # --------------------------
        # INSERT GROCERY ITEMS
        # --------------------------

        cursor.execute("""
        INSERT OR REPLACE INTO grocery_items 
        (id, household_id, name, category, quantity, purchase_date, expiry_date)
        VALUES (1, 1, 'Milk', 'Dairy', 1, '2026-04-20', '2026-04-28')
        """)

        cursor.execute("""
        INSERT OR REPLACE INTO grocery_items 
        (id, household_id, name, category, quantity, purchase_date, expiry_date)
        VALUES (2, 1, 'Bread', 'Bakery', 1, '2026-04-20', '2026-04-22')
        """)

        conn.commit()
        conn.close()

    def test_valid_output(self):
        result = get_item_risk(1)
        self.assertIn(result, ["Safe", "At Risk"])

    def test_multiple_inputs(self):
        result1 = get_item_risk(1)
        result2 = get_item_risk(2)

        self.assertIn(result1, ["Safe", "At Risk"])
        self.assertIn(result2, ["Safe", "At Risk"])

    def test_invalid_item(self):
        result = get_item_risk(999)
        self.assertIn(result, ["Safe", "At Risk"])


if __name__ == "__main__":
    unittest.main()