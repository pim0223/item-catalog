from flask import Flask, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)

login_manager = LoginManager(app)
login_manager.login_view = 'index'

@login_manager.unauthorized_handler
def unauthorized():
    flash('You need to be logged in to view this page')
    return redirect(url_for('index'))

from src.oauth.routes import bp as google_blueprint
from src.catalog.routes import bp as catalog_blueprint

app.register_blueprint(catalog_blueprint, url_prefix="/catalog")
app.register_blueprint(google_blueprint, url_prefix="/login")

@app.route('/')
def index():
    return redirect(url_for('catalog.show_all_items'))