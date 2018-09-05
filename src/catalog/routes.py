from flask import Flask, request, render_template, redirect, url_for, flash, session, Blueprint
import uuid
from src.models import Item, Category
from src.catalog.forms import ItemForm
from src import db
from flask_login import login_required, current_user

bp = Blueprint('catalog', __name__)

@bp.route('/')
@bp.route('/items')
def show_all_items():
    items = Item.query.order_by(Item.created_at.desc()).limit(10).all()
    categories = Category.query.all()
    return render_template('catalog/catalog.html', items=items, categories=categories, title='All items')

@bp.route('/categories/<category_name>/')
def show_items_category(category_name):
    category = Category.query.filter_by(name=category_name).one()
    items = Item.query.filter_by(category=category).all()
    return render_template('catalog/category.html', items=items, category=category, title='Items in category'.format(category_name))

@bp.route('/items/<item_name>/', methods=['GET'])
def view_item(item_name):
    item = Item.query.filter_by(name=item_name).one()
    return render_template('catalog/view_item.html', item=item, title=item_name, current_user=current_user)

@bp.route('/items/add/', methods=['GET','POST'])
@login_required
def add_item():
    form = ItemForm()
    if request.method == 'GET':
        return render_template('catalog/add_item.html', form=form, title='Add item')
    else:
        
        item = Item(
            name = form.data['name'],
            description = form.data['description'],
            category_id = form.data['category'],
            creator = current_user
            )
        db.session.add(item)
        db.session.commit()
        flash('Item added successfully!')

        return(redirect(url_for('catalog.show_all_items')))

@bp.route('/items/<item_name>/edit/', methods=['GET','POST'])
@login_required
def edit_item(item_name):
    item = Item.query.filter_by(name=item_name).one()

    if current_user != item.creator:
        flash("You are not authorized to edit this item, as you didn't create it!")
        return redirect(url_for('catalog.view_item', item_name=item_name))

    form = ItemForm(name=item.name, description=item.description, category=item.category.name, title='Edit item')

    if request.method == 'GET':
        return render_template('catalog/edit_item.html', form=form)
    else:
        item.name = form.data['name']
        item.description = form.data['description']
        item.category_id = form.data['category']
        db.session.add(item)
        db.session.commit()
        flash('Item edited successfully!')

        return(redirect(url_for('catalog.show_all_items')))

@bp.route('/items/<item_name>/delete/', methods=['GET','POST'])
@login_required
def delete_item(item_name):
    item = Item.query.filter_by(name=item_name).one()

    if current_user != item.creator:
        flash("You are not authorized to delete this item, as you didn't create it!")
        return redirect(url_for('catalog.view_item', item_name=item_name))

    if request.method == 'GET':
        return render_template('catalog/delete_item.html', item=item, title='Delete item')
    else:
        db.session.delete(item)
        db.session.commit()
        flash('Item deleted successfully!')

        return(redirect(url_for('catalog.show_all_items')))