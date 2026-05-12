import numpy as np
from sklearn.linear_model import LogisticRegression
from utils.db import execute_query


class MLModelEngine:

    def __init__(self):
        self.model = LogisticRegression()

    def prepare_training_data(self):
        query = """
        SELECT days_since_purchase, days_to_expiry, usage_frequency, label
        FROM ml_training_data
        """
        rows = execute_query(query, fetch=True)

        if not rows or len(rows) < 5:
            return None, None

        X = []
        y = []

        for row in rows:
            X.append([
                row['days_since_purchase'],
                row['days_to_expiry'],
                row['usage_frequency']
            ])
            y.append(row['label'])

        return np.array(X), np.array(y)

    def train_model(self):
        X, y = self.prepare_training_data()

        if X is None:
            return False

        self.model.fit(X, y)
        return True

    def predict_risk(self, days_since_purchase, days_to_expiry, usage_frequency):
        try:
            features = np.array([[days_since_purchase, days_to_expiry, usage_frequency]])
            prediction = self.model.predict(features)[0]
            probability = self.model.predict_proba(features)[0][1]

            return {
                "label": "At Risk" if prediction == 1 else "Safe",
                "probability": float(probability)
            }
        except:
            return {
                "label": "Safe",
                "probability": 0.0
            }

    def save_training_sample(self, item_id, days_since_purchase, days_to_expiry, category, usage_frequency, label):
        query = """
        INSERT INTO ml_training_data 
        (item_id, days_since_purchase, days_to_expiry, category, usage_frequency, label)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        execute_query(query, (
            item_id,
            days_since_purchase,
            days_to_expiry,
            category,
            usage_frequency,
            label
        ), commit=True)

    def calculate_usage_frequency(self, item_id):
        query = """
        SELECT COUNT(*) as count
        FROM item_usage
        WHERE item_id = ?
        """
        result = execute_query(query, (item_id,), fetch=True)

        if result and result[0]['count'] is not None:
            return float(result[0]['count'])
        return 0.0