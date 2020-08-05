from app import app
from flask import render_template


@app.route('/')
def render_main():
    return render_template('main.html')


@app.route('/cart/')
def render_cart():
    return render_template('cart.html')


@app.route('/account/')
def render_account():
    return render_template('account.html')


@app.route('/login/')
def render_login():
    return render_template('login.html')


@app.route('/register')
def render_register():
    return render_template('register.html')


@app.route('/logout')
def render_logout():
    return render_template('login.html')


@app.route('/ordered/')
def render_ordered():
    return render_template('ordered.html')
