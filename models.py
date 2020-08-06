from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

dishes_list = db.Table(
    'dishes_list',
    db.Column("dish_id", db.Integer, db.ForeignKey('dish.id')),
    db.Column("order_id", db.Integer, db.ForeignKey('order.id')),
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False, unique=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))


class Dish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, unique=True)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String, nullable=False, unique=True)
    picture = db.Column(db.String, nullable=False, unique=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    orders = db.relationship('Order', secondary=dishes_list, back_populates='dishes')


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, unique=True)
    dish = db.relationship('Dish')


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    order_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    phone = db.Column(db.String, nullable=False, unique=True)
    address = db.Column(db.String, nullable=False, unique=True)
    users = db.relationship('User')
    dishes = db.relationship('Dish', secondary=dishes_list, back_populates='orders')
