from src import app, db
from src.models import User, Item, Category, OAuth

# Add some categories, if they are not present yet
names = ['Football', 'Tennis', 'Basketball', 'Hockey',
         'Climbing', 'Wrestling', 'Boxing', 'Skiing',
         'Snowboarding', 'Surfing']

for name in names:
    if not Category.query.filter_by(name=name).all():
        db.session.add(Category(name=name))
        db.session.commit()


# For debugging
@app.shell_context_processor
def make_shell_context():
    return {'db': db,
            'User': User,
            'Item': Item,
            'Category': Category,
            'OAuth': OAuth}
