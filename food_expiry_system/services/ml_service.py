from models.ml_model import MLModelEngine
from models.grocery_item import (
    calculate_days_since_purchase,
    calculate_days_to_expiry,
    get_usage_history
)

# Initialize single model instance
ml_engine = MLModelEngine()
model_trained = False


def get_usage_frequency(item_id):
    history = get_usage_history(item_id)
    return float(len(history)) if history else 0.0


def train_model_if_needed():
    global model_trained

    if not model_trained:
        trained = ml_engine.train_model()
        model_trained = trained
        return trained

    return True


def get_item_risk(item):
    # ensure model is trained
    train_model_if_needed()

    try:
        days_since_purchase = calculate_days_since_purchase(item['purchase_date'])
        days_to_expiry = calculate_days_to_expiry(item['expiry_date'])
        usage_frequency = get_usage_frequency(item['id'])

        result = ml_engine.predict_risk(
            days_since_purchase,
            days_to_expiry,
            usage_frequency
        )

        # add simple reason tags
        reasons = []

        if days_to_expiry <= 2:
            reasons.append("Near expiry")

        if usage_frequency == 0:
            reasons.append("Not used recently")

        if result['probability'] > 0.7:
            reasons.append("High risk pattern")

        result['reasons'] = reasons

        return result

    except:
        return {
            "label": "Safe",
            "probability": 0.0,
            "reasons": []
        }


def save_training_from_item(item, label):
    try:
        days_since_purchase = calculate_days_since_purchase(item['purchase_date'])
        days_to_expiry = calculate_days_to_expiry(item['expiry_date'])
        usage_frequency = get_usage_frequency(item['id'])

        ml_engine.save_training_sample(
            item_id=item['id'],
            days_since_purchase=days_since_purchase,
            days_to_expiry=days_to_expiry,
            category=item['category'],
            usage_frequency=usage_frequency,
            label=label
        )
    except:
        pass


def retrain_model():
    global model_trained
    model_trained = ml_engine.train_model()
    return model_trained