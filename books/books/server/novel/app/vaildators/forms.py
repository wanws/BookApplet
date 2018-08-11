"""
    Created by Amirk on 2018-07-30.
"""

from wtforms import Form, StringField, IntegerField

from wtforms.validators import DataRequired


class UserInfoForm(Form):
    code = StringField(validators=[DataRequired()])
    encryptedData = StringField(validators=[DataRequired()])
    userinfo = StringField(validators=[DataRequired()])


class BookDetailForm(Form):
    bookid = StringField(validators=[DataRequired()])


class BookSectionForm(BookDetailForm):
    page = IntegerField(validators=[DataRequired()])


class UserBookCaseForm(BookDetailForm):
    type = IntegerField()


class ContentTextForm(Form):
    query = StringField(validators=[DataRequired()])


class BookByCategorieForm(Form):
    name = StringField(validators=[DataRequired()])
    gender = StringField(validators=[DataRequired()])
    type = StringField(validators=[DataRequired()])
    start = IntegerField()
