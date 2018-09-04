from flask import Flask
from config import Config

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)

from src.oauth.routes import bp as google_blueprint
from src.catalog.routes import bp as catalog_blueprint

app.register_blueprint(catalog_blueprint, url_prefix="/catalog")
app.register_blueprint(google_blueprint, url_prefix="/login")