from datetime import datetime
from flask_login import UserMixin
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin
from marshmallow import Schema, fields
from src import db

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired
from wtforms_alchemy import ModelForm


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), index=True, unique=True)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    items = db.relationship('Item', backref='creator')

    def __repr__(self):
        return self.email


# Defines an OAuth record (user and token combination)
class OAuth(OAuthConsumerMixin, db.Model):
    provider_user_id = db.Column(db.String(256), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True)
    items = db.relationship('Item', backref='category')
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return self.name


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True)
    description = db.Column(db.String(1000))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return self.name


# To return items in the REST API
class ItemSchema(Schema):
    id = fields.Integer()
    name = fields.Str()
    description = fields.Str()
    created_at = fields.DateTime()
    creator = fields.Str()
    category = fields.Str()


# Form to add new items
class ItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    category = SelectField('Category', validators=[DataRequired()],
                           choices=[(category.id, category.name) for
                                    category in Category.query.all()])
    submit = SubmitField('Submit')
