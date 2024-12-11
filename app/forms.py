from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms.fields import (
    BooleanField,
    DateField,
    StringField,
    SubmitField,
    TextAreaField,
    TimeField,
)
from wtforms.validators import DataRequired
from datetime import datetime


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

    def validate_end_date(form, _field):
        start_datetime = datetime.combine(
            form.start_date.data, form.start_time.data
        )
        end_datetime = datetime.combine(
            form.end_date.data, form.end_time.data
        )
        if end_datetime <= start_datetime:
            msg = "end must be after start"
            raise ValidationError(msg)
