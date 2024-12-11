from flask_wtf import FlaskForm
from wtforms.fields import (
    BooleanField,
    DateField,
    StringField,
    SubmitField,
    TextAreaField,
    TimeField,
)
from wtforms.validators import DataRequired


class AppointmentForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    start_date = DateField("start date", validators=[DataRequired()])
    start_time = TimeField("start time", validators=[DataRequired()])
    end_date = DateField("end date", validators=[DataRequired()])
    end_time = TimeField("end time", validators=[DataRequired()])
    description = TextAreaField(
        "description", validators=[DataRequired()]
    )
    private = BooleanField("private")
    submit = SubmitField("create appointment")
