""" TODO: add more field for filtering and search criteria """
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, Email, Length, Optional, URL


class SearchForm(FlaskForm):
    """ forms for searching for a trip"""

    origin = StringField("From", validators=[InputRequired(),
                                             Length(min=2, max=30)])
    checkin = DateField("Check in date", format='yyyy-mm-dd',
                        validators=[InputRequired()])
    checkout = DateField("Check out date", format='yyyy-mm-dd',
                         validators=[InputRequired()])
    adults = IntegerField("Number of guests",
                          validators=[InputRequired(), Length(min=1, max=10)])

