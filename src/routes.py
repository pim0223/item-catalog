from flask import Flask, request
from src import app

@app.route('/')
@app.route('/catalog/')
def show_all_items():
    return 'Here you can see all the items in the db'

@app.route('/catalog/<category_name>/')
def show_items_category(category_name):
    return 'Here you can see all items in the {} category'.format(category_name)

@app.route('/catalog/<item_name>/', methods=['GET'])
def view_item(item_name):
    return 'Here you can see item {}'.format(item_name)

@app.route('/catalog/<item_name>/edit/', methods=['GET','POST'])
def edit_item(item_name):
    pass

@app.route('/catalog/<item_name>/delete/', methods=['GET','POST'])
def delete_item(item_name):
    pass