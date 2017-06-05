#-*- coding: utf-8 -*-
__author__ = 'rdk'

from flask_wtf import Form
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired


class ProjectForm(Form):
    customer = SelectField('Customer', coerce=int, validators=[DataRequired()])
    code = StringField(u'Project Code', validators=[DataRequired()],
                       render_kw={"placeholder" : "Project Code", "required" : "true"})
    description = StringField(u'Project Description', validators=[DataRequired()],
                              render_kw={"placeholder" : "Project Description", "required" : "true"})