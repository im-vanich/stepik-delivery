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
        if user.email == email:
            error_msg = "Пользователь с указанным именем уже существует"
            return render_template('register.html', error_msg=error_msg, form=form)
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        session['is_auth'] = True
        flash('Аккаунт создан', 'success')
        return redirect(url_for('render_main'))
    return render_template('register.html', form=form)


@app.route('/login/', methods=['POST', 'GET'])
def render_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.email == form.email.data).first()
        if user and user.password_valid(form.password.data):
            session['email'] = user.email
            session['is_auth'] = True
            return redirect(url_for('render_main'))
        return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@app.route('/')
def render_main():
    category_list = db.session.query(Category).all()
    is_auth = session.get('is_auth')
    category_dish = {}
    for i in range(1, len(category_list) + 1):
        category_dish[i] = [item for item in db.session.query(Dish).filter(Dish.category_id == i).limit(3)]
    return render_template('main.html', category_dish=category_dish, category_list=category_list, is_auth=is_auth)


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
        user = db.session.query(User).filter(User.email == form.email.data).first()
        if user and is_auth:  # Если пользователь залогинен добавляем заказ в базу
            order = Order(date=date.today(), order_price=total_price, status='ok', email=email, phone=phone,
                          address=address, users_id=user.id)
            db.session.add(order)
            for d in dish:
                if d.id in dish_list:
                    order.dishes.append(d)
            db.session.commit()
            flash('Заказ принят в работу', 'success')
        else:
            return render_template('cart.html', is_auth=is_auth, form=form, count=total_count, price=total_price,
                                   cart_list=cart_list)
        return redirect(url_for('render_ordered'))
    return render_template('cart.html', form=form, count=total_count, price=total_price, cart_list=cart_list,
                           is_auth=is_auth)


@app.route('/account/')
def render_account():
    is_auth = session.get('is_auth')
    email = session.get('email')
    user = User.query.filter(User.email == email).first()
    orders = Order.query.filter(Order.users_id == user.id).all()  # получаем список всех заказов пользователя
    dishes = Dish.query.all()  # получаем список всех блюд
    dl = db.session.query(dishes_list).all()  # получаем таблицу many to many отношения закозов и блю в них
    new_orders = {}  # создаем пустой словарь для хранения блюд, для каждого заказа
    for i in orders:
        for j in dl:
            if j[1] == i.id:
                new_orders.setdefault(i.id, []).append(dishes[j[0] - 1])  # записывем блюда в словарь
    print(new_orders)
    return render_template('account.html', is_auth=is_auth, orders=new_orders)


@app.route('/logout/')
def render_logout():
    session['is_auth'] = False
    is_auth = session.get('is_auth')
    session['cart'] = []
    category_list = db.session.query(Category).all()
    category_dish = {}
    for i in range(1, len(category_list) + 1):
        category_dish[i] = [item for item in db.session.query(Dish).filter(Dish.category_id == i).limit(3)]
    return render_template('main.html', is_auth=is_auth, category_list=category_list, category_dish=category_dish)


@app.route('/category/')
def render_category():
    is_auth = session.get('is_auth')
    category_list = db.session.query(Category).all()
    dishes_items = db.session.query(Dish).all()
    return render_template('category.html', category_list=category_list, dishes_items=dishes_items, is_auth=is_auth)


@app.route('/ordered/')
def render_ordered():
    return render_template('ordered.html')
