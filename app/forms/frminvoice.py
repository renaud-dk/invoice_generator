#-*- coding: utf-8 -*-
__author__ = 'rdk'

from flask_wtf import Form
from wtforms import StringField, SelectField, BooleanField
from wtforms.validators import DataRequired


class InvoiceForm(Form):
    customer = SelectField('Customer', coerce=int, validators=[DataRequired()])
    date_from = StringField('Date From', validators=[DataRequired()],
                       render_kw={"class": "span2", "placeholder": "Date from", "required": "true"})
    date_to = StringField('Date To', validators=[DataRequired()],
                            render_kw={"class": "span2", "placeholder": "Date to", "required": "true"})

    is_official = BooleanField('Increment invoice number')