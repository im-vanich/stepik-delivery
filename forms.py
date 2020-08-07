from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class OrderForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired(), Length(min=2, max=20)])
    address = StringField('Адрес', validators=[DataRequired(), Length(min=5)])
    email = StringField('Электропочта', validators=[DataRequired(), Email()])
    phone = StringField('Телефон', validators=[DataRequired(), Length(min=6)])
    order = SubmitField('Оформить заказ')


class RegistrationForm(FlaskForm):
    email = StringField('Электропочта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=5)])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])
    register = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = StringField('Электропочта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=5)])
    register = SubmitField('Войти')
