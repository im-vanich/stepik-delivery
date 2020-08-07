from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class OrderForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired(), Length(min=2, max=20)])
    address = StringField('Адрес', validators=[DataRequired(), Length(min=5)])
    email = StringField('Электропочта', validators=[DataRequired(), Email()])
    phone = StringField('Телефон', validators=[DataRequired(), Length(min=6)])
    order = SubmitField('Оформить заказ')
