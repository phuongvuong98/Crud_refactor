from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import (DataRequired, Regexp, Length)


class CityForm(FlaskForm):
    city_name = StringField(
        'city_name',
        [DataRequired(), Regexp(r'[A-Za-z]'), Length(min=4, max=25)]
    )
