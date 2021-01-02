from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, Email, Length, Optional, URL


class SearchForm(FlaskForm):
    """ forms for searching for a trip"""

    origin = StringField("from", validators=[InputRequired(),
                                             Length(min=2, max=30)])
    checkin = DateField("check in date", validators=[InputRequired()])
    checkout = DateField("check out date", validators=[InputRequired()])
    adults = IntegerField("number of guests",
                          validators=[InputRequired(), Length(min=1, max=10)])
    

