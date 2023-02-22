from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, SelectField, \
    IntegerField, DateField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    job = StringField('Описание работы')
    work_size = IntegerField('Объём работы, ч')
    collaborators = StringField('Соучастники')
    start_date = DateField('Начало работы')
    end_date = DateField('Конец работы')
    is_finished = BooleanField('Завершена')
    submit = SubmitField('Применить')
