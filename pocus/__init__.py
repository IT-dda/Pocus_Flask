from flask import Flask
from pocus import database
from .views import database_views, main_views, upper_views, lower_views


def create_app():
    app = Flask(__name__)

    # blueprint
    app.register_blueprint(main_views.bp)
    app.register_blueprint(database_views.bp)
    app.register_blueprint(upper_views.bp)
    app.register_blueprint(lower_views.bp)

    return app