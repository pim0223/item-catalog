from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired
from src.models import Category

# Form to add new items
class ItemForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    category = SelectField("Category", validators=[DataRequired()],
                           choices=[(category.id, category.name) for
                                    category in Category.query.all()])
    submit = SubmitField("Submit")
