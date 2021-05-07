from flask_security.forms import Required
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import URL


class TaskForm(FlaskForm):
    """Форма для указания URL"""
    url = StringField('Введите адрес страницы:', validators=[Required(), URL()])
