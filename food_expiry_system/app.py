from flask import Flask
from config import SECRET_KEY
from utils.db import init_db

from routes.auth_routes import auth_bp
from routes.household_routes import household_bp
from routes.grocery_routes import grocery_bp
from routes.dashboard_routes import dashboard_bp
from routes.alert_routes import alert_bp
from routes.admin_routes import admin_bp


def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY

    init_db()

    app.register_blueprint(auth_bp)
    app.register_blueprint(household_bp)
    app.register_blueprint(grocery_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(alert_bp)
    app.register_blueprint(admin_bp)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)