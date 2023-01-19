from flask import Flask
import os
from . import filters

def create_app():
    app = Flask(__name__)
    app.jinja_env.filters['nl2br'] = filters.nl2br
    app.secret_key = os.environ["SECRET_KEY"]
    from .views import views

    app.register_blueprint(views, url_prefix="/")

    return app
