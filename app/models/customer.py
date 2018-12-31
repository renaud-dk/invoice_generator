#-*- coding: utf-8 -*-
__author__ = 'rdk'

from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index = True, unique = True)
    address = db.Column(db.String(255), nullable = True)
    city = db.Column(db.String(64), nullable = True)
    zip_code = db.Column(db.Integer, nullable = True)
    country = db.Column(db.String(64), nullable = True)
    vat = db.Column(db.String(32))
    rate = db.Column(db.Integer)
    presta_import_fmt = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return '<Customer %r>' % (self.name)
