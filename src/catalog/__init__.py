from flask import Blueprint

bp = Blueprint('catalog', __name__)

from src.catalog import routes