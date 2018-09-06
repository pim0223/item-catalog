# JSON API to GET items / item by id

from flask import Blueprint, jsonify
from src.models import Item, ItemSchema

bp = Blueprint("api", __name__)


# Get all items
@bp.route("/items", methods=["GET"])
def get_items():
    items = Item.query.all()
    items_schema = ItemSchema(many=True)
    return jsonify(items_schema.dump(items))


# Get an item by ID
@bp.route("/item/<id>", methods=["GET"])
def get_item(id):
    item = Item.query.get(id)
    item_schema = ItemSchema()
    return jsonify(item_schema.dump(item))
