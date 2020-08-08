from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
# Таблица отношения блюд и заказов
dishes_list = db.Table(
    'dishes_list',
    db.Column("dish_id", db.Integer, db.ForeignKey('dish.id')),
    db.Column("order_id", db.Integer, db.ForeignKey('order.id')),
)


# Таблица пользователя
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False, unique=True)
    orders = db.relationship('Order')

    @property
    def password(self):
        raise AttributeError("Вам не нужно знать пароль!")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def password_valid(self, password):
        return check_password_hash(self.password_hash, password)


# Таблица блюд
class Dish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, unique=True)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String, nullable=False, unique=True)
    picture = db.Column(db.String, nullable=False, unique=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    orders = db.relationship('Order', secondary=dishes_list, back_populates='dishes')


# Таблица категорий
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, unique=True)
    dish = db.relationship('Dish')


# Таблица заказа
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    order_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    users_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    dishes = db.relationship('Dish', secondary=dishes_list, back_populates='orders')
