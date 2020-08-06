import random
from app import app, db
from flask import render_template, session
from models import User, Category, Dish, Order, dishes_list
from forms import OrderForm


@app.route('/')
def render_main():
    category_list = db.session.query(Category).all()
    dishes_items = db.session.query(Dish).all()
    return render_template('main.html', category_list=category_list, dishes_items=dishes_items)


@app.route('/cart/', methods=['POST', 'GET'])
def render_cart():
    form = OrderForm()
    return render_template('cart.html', form=form)


@app.route('/account/')
def render_account():
    return render_template('account.html')


@app.route('/login/')
def render_login():
    return render_template('login.html')


@app.route('/register/')
def render_register():
    return render_template('register.html')


@app.route('/logout/')
def render_logout():
    return render_template('auth.html')


@app.route('/ordered/')
def render_ordered():
    return render_template('ordered.html')
