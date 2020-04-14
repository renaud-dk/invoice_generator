#-*- coding: utf-8 -*-

from api.app import db
from .base_model import BaseModel

class Project(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64), index = True, unique = True)
    description = db.Column(db.String(255), nullable = True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable = False)
    customer = db.relationship('Customer', backref=db.backref('projects', cascade="all, delete-orphan"), lazy='joined')
