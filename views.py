from collections import Counter
from app import app, db
from flask import render_template, flash, redirect, url_for, session
from models import User, Category, Dish, Order, dishes_list
from forms import OrderForm


@app.route('/')
def render_main():
    category_list = db.session.query(Category).all()
    dishes_items = db.session.query(Dish).all()
    return render_template('main.html', category_list=category_list, dishes_items=dishes_items)


@app.route('/addtocart/<int:dish_id>')
def add_to_cart(dish_id):
    cart = session.get('cart', [])
    cart.append(dish_id)
    session['cart'] = cart
    return redirect(url_for('render_cart'))


@app.route('/removetocart/<int:dish_id>')
def remove_to_cart(dish_id):
    cart = session.get('cart', [])
    dish_index = cart.index(dish_id)
    cart.pop(dish_index)
    session['cart'] = cart
    return redirect(url_for('render_cart'))


@app.route('/cart/', methods=['POST', 'GET'])
def render_cart():
    form = OrderForm()
    cart = session.get('cart')
    cart_list = []
    for dish_id in cart:
        cart_list.append(db.session.query(Dish).filter(Dish.id == dish_id).first())
    total_count = 0
    total_price = 0
    for i in cart_list:
        total_price += i.price
        total_count += 1
    print(total_price)
    if form.validate_on_submit():
        flash('Заказ принят в работу', 'success')
        return redirect(url_for('render_ordered'))
    return render_template('cart.html', form=form, count=total_count, price=total_price, cart_list=cart_list)


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
