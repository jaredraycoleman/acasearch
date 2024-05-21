from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Optional

class ConferenceForm(FlaskForm):
    acronym = StringField('Acronym', validators=[DataRequired()])
    h5_index = IntegerField('H5 Index', validators=[Optional()])
    core_rank = StringField('CORE Rank', validators=[Optional()])
    era_rank = StringField('ERA Rank', validators=[Optional()])
    qualis_rank = StringField('QUALIS Rank', validators=[Optional()])
    deadline = DateField('Deadline', validators=[Optional()])
    notification_date = DateField('Notification Date', validators=[Optional()])
    start_date = DateField('Start Date', validators=[Optional()])
    end_date = DateField('End Date', validators=[Optional()])
    location = StringField('Location', validators=[Optional()])
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    submit = SubmitField('Submit')
