#-*- coding: utf-8 -*-
__author__ = 'rdk'

from flask_wtf import Form
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired


class CustomerForm(Form):
    name = StringField('Name', validators=[DataRequired()],
                       render_kw={"placeholder": "Customer name", "required": "true"})
    address = StringField('Address', render_kw={"placeholder": "Customer Address"})
    city = StringField('City', render_kw={"placeholder": "Customer City"})
    zip_code = IntegerField('Zip code', render_kw={"placeholder": "Customer Zip code"})
    country = StringField('Country', render_kw={"placeholder": "Customer Country"})
    vat = StringField('VAT', validators=[DataRequired()],
                      render_kw={"placeholder": "Customer VAT", "required": "true"})