from src import app, db
from src.catalog.models import User, Item, Category

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Item': Item, 'Category': Category,}