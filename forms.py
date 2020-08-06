from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class OrderForm(FlaskForm):
    name = StringField('Имя')
    address = StringField('Адрес')
    email = StringField('Электропочта')
    phone = StringField('Телефон')
    order = SubmitField('Оформить заказ')
