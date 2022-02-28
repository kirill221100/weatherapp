from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField

class OptionsForm(FlaskForm):
    option = RadioField('Система измерений', choices=[('standart', 'Стандартная'), ('imperial', 'Имперская'), ('metric', 'Метричная')])
    submit = SubmitField('Применить')
