from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    team_leader = StringField('Руководитель команды', validators=[DataRequired()])
    job = StringField('Название работы', validators=[DataRequired()])
    work_size = IntegerField('Объём работы', validators=[DataRequired()])
    collaborators = StringField('Участники', validators=[DataRequired()])
    is_finished = BooleanField("Завершено")
    submit = SubmitField('Применить')