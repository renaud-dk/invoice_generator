# -*- coding: utf-8 -*-

from api.app import db
from .base_model import BaseModel

class Customer(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index = True, unique = True)
    address = db.Column(db.String(255), nullable = True)
    city = db.Column(db.String(64), nullable = True)
    zip_code = db.Column(db.Integer, nullable = True)
    country = db.Column(db.String(64), nullable = True)
    vat = db.Column(db.String(32))
    rate = db.Column(db.Integer)
    presta_import_fmt = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    _hidden_fields = [
        "user_id", 
        "presta_import_fmt"
    ]
    