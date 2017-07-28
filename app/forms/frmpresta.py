#-*- coding: utf-8 -*-
__author__ = 'rdk'

from flask_wtf import Form
from wtforms import StringField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired

class PrestaFrom(Form):
    id = IntegerField('Presta Id', id="prestaid", render_kw={"type":"hidden"})
    project = SelectField('Project', coerce=int, validators=[DataRequired()],
                          render_kw={"placeholder": "Select a project", "required":"true"})
    date = StringField('Date', validators=[DataRequired()],
                     render_kw={"class":"span2", "placeholder": "Presta start date and time", "required": "true"})
    duration = StringField('Duration', validators=[DataRequired()],
                             render_kw={"class": "timepicker", "required": "true"})
    comment = TextAreaField('Comment', validators=[DataRequired()],
                            render_kw={"placeholder": "Presta comment", "required": "true"})
    travel_distance = IntegerField('Travel distande',render_kw={"placeholder": "Travel distance", "pattern":"number"})
    travel_comment = TextAreaField('Travel comment', render_kw={"placeholder": "Travel description"})