from flask import Flask, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

from config import Config

# Initiate app
app = Flask(__name__)

# Set app configuration
app.config.from_object(Config)

# Set up database, migrations, bootstrap UI and the login manager
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)
login_manager = LoginManager(app)

# Register the login blueprint
from src.oauth.routes import bp as google_blueprint  # noqa
app.register_blueprint(google_blueprint, url_prefix="/login")

# Register the catalog blueprint
from src.catalog.routes import bp as catalog_blueprint  # noqa
app.register_blueprint(catalog_blueprint, url_prefix="/catalog")

# Register the API blueprint
from src.api.routes import bp as api_blueprint  # noqa
app.register_blueprint(api_blueprint, url_prefix="/api")


# The root redirects to catalog
@app.route('/')
def index():
    return redirect(url_for('catalog.view_all_items'))
