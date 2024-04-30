import wtforms
from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField, EmailField
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired


class DepartmentForm(FlaskForm):
    title = StringField('Назввание департамента', validators=[DataRequired()])
    chief = StringField('Руководитель департамента', validators=[DataRequired()])
    members = StringField('Участники', validators=[DataRequired()])
    email = EmailField("Email",validators=[DataRequired()])
    submit = SubmitField('Применить')