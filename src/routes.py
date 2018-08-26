from flask import Flask, request, render_template, redirect, url_for, flash
from src.models import Item, Category
from src.forms import ItemForm
from src import app, db

@app.route('/')
@app.route('/catalog/')
@app.route('/catalog/items/')
def show_all_items():
    items = Item.query.order_by(Item.created_at.desc()).limit(10).all()
    categories = Category.query.all()
    return render_template('catalog.html', items=items, categories=categories, title='All items')

@app.route('/catalog/categories/<category_name>/')
def show_items_category(category_name):
    category = Category.query.filter_by(name=category_name).one()
    items = Item.query.filter_by(category=category).all()
    return render_template('category.html', items=items, category=category)

@app.route('/catalog/items/<item_name>/', methods=['GET'])
def view_item(item_name):
    item = Item.query.filter_by(name=item_name).one()
    return render_template('view_item.html', item=item)

@app.route('/catalog/items/add/', methods=['GET','POST'])
def add_item():
    form = ItemForm()
    if request.method == 'GET':
        return render_template('add_item.html', form=form)
    else:
        item = Item(
            name = form.data['name'],
            description = form.data['description'],
            category_id = form.data['category']
            )
        db.session.add(item)
        db.session.commit()
        flash('Item added successfully!')

        return(redirect(url_for('show_all_items')))

@app.route('/catalog/items/<item_name>/edit/', methods=['GET','POST'])
def edit_item(item_name):
    item = Item.query.filter_by(name=item_name).one()
    form = ItemForm(name=item.name, description=item.description, category=item.category.name)

    if request.method == 'GET':
        return render_template('edit_item.html', form=form)
    else:
        item.name = form.data['name']
        item.description = form.data['description']
        item.category_id = form.data['category']
        db.session.add(item)
        db.session.commit()
        flash('Item edited successfully!')

        return(redirect(url_for('show_all_items')))

@app.route('/catalog/items/<item_name>/delete/', methods=['GET','POST'])
def delete_item(item_name):
    item = Item.query.filter_by(name=item_name).one()

    if request.method == 'GET':
        return render_template('delete_item.html', item=item)
    else:
        db.session.delete(item)
        db.session.commit()
        flash('Item deleted successfully!')

        return(redirect(url_for('show_all_items')))