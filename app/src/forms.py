from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField, RadioField, FormField, FieldList, FileField
from wtforms.validators import Length, DataRequired, Email, EqualTo, ValidationError
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms_sqlalchemy.fields import QuerySelectMultipleField, QuerySelectField
from flask_wtf.file import FileAllowed

from app import db
import sqlalchemy as sqla

class ParseForm(FlaskForm):
    link = StringField('Paste link', validators=[DataRequired()])
    file = FileField('Upload spreadsheet', validators=[DataRequired(), FileAllowed(["xlsx"], "XLSX only!")])
    submit = SubmitField('Transfer content')