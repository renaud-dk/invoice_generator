#-*- coding: utf-8 -*-
__author__ = 'rdk'

from flask_wtf import Form
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired


class UploadForm(Form):
    filetype = SelectField('Filetype', coerce=int, validators=[DataRequired()])

    # TODO used FileFiedl instead of StringField
    filename = StringField('Select file', validators=[DataRequired()],
                           render_kw={"class":"show-for-sr", "type":"file", "accept":".csv",
                                      "required": "true"})