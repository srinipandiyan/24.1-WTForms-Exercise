"""Pet Adoption Agency Application Forms"""

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField, BooleanField
from wtforms.validators import InputRequired, Length, NumberRange, URL, Optional


class AddPetForm(FlaskForm):
    """Form for adding new pets to index."""

    name = StringField(
        "Pet Name",
        validators=[InputRequired()])

    species = SelectField(
        "Species",
        choices=[("cat", "Cat"), ("dog", "Dog"), ("porcupine", "Porcupine")])

    photo_url = StringField(
        "Photo URL",
        validators=[Optional(), URL()])

    age = IntegerField(
        "Age in years",
        validators=[Optional(), NumberRange(min=0, max=25)])

    notes = TextAreaField(
        "Notes",
        validators=[Optional(), Length(min=10)])


class EditPetForm(FlaskForm):
    """Form for editing an existing pet within index."""

    photo_url = StringField(
        "Photo URL",
        validators=[Optional(), URL()])

    notes = TextAreaField(
        "Notes",
        validators=[Optional(), Length(min=10)])

    available = BooleanField("Available?")