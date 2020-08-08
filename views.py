from datetime import date
from app import app, db
from flask import render_template, flash, redirect, url_for, session
from models import User, Category, Dish, Order, dishes_list
from forms import OrderForm, RegistrationForm, LoginForm


@app.route('/register/', methods=['GET', 'POST'])
def render_register():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter(email == email).first()
        if user:
            error_msg = "Пользователь с указанным именем уже существует"
            return render_template('register.html', error_msg=error_msg, form=form)
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        session['is_auth'] = True
        is_auth = session.get('is_auth')
        flash('Аккаунт создан', 'success')
        return redirect(url_for('render_main', is_auth=is_auth))
    return render_template('register.html', form=form)


@app.route('/login/', methods=['POST', 'GET'])
def render_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(email=form.email.data).first()
        if user and user.password_valid(form.password.data):
            session['user'] = {
                'id': 'user.id',
                'email': 'user.email'
            }
            session['is_auth'] = True
            return redirect(url_for('render_main'))
        return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@app.route('/')
def render_main():
    category_list = db.session.query(Category).all()
    dishes_items = db.session.query(Dish).all()
    is_auth = session.get('is_auth')
    return render_template('main.html', category_list=category_list, dishes_items=dishes_items, is_auth=is_auth)


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
    is_auth = session.get('is_auth')
    form = OrderForm()
    cart = session.get('cart')
    cart_list = []  # список для страницы корзины
    dish_list = []  # список id для страницы аккаунта
    for dish_id in cart:
        cart_list.append(db.session.query(Dish).filter(Dish.id == dish_id).first())  #
    total_count = 0
    total_price = 0
    for i in cart_list:
        total_price += i.price  # считаем общую стоимость и количество товаров в заказе
        total_count += 1
        dish_list.append(i.id)
    if form.validate_on_submit():
        email = form.email.data
        phone = form.phone.data
        address = form.address.data
        dish = Dish.query.all()
        user = db.session.query(User).filter(User.email == email).first()
        order = Order(date=date.today(), order_price=total_price, status='ok', email=email, phone=phone,
                      address=address, users_id=user.id)
        db.session.add(order)
        for d in dish:
            if d.id in dish_list:
                order.dishes.append(d)
        db.session.commit()
        flash('Заказ принят в работу', 'success')
        return redirect(url_for('render_ordered'))
    return render_template('cart.html', form=form, count=total_count, price=total_price, cart_list=cart_list,
                           is_auth=is_auth)


@app.route('/logout/')
def render_logout():
    session['is_auth'] = False
    is_auth = session.get('is_auth')
    return render_template('main.html', is_auth=is_auth)


@app.route('/account/')
def render_account():
    is_auth = session.get('is_auth')
    email = session.get('email')
    order_list_query = Order.query.filter(email == email).first()  # получаем заказ пользователя
    ls = Order.query.filter(Order.id == order_list_query.id).scalar()
    print(ls.dishes.dish_id)

    return render_template('account.html', is_auth=is_auth)


@app.route('/ordered/')
def render_ordered():
    return render_template('ordered.html')
