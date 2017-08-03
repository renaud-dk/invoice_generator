#-*- coding: utf-8 -*-
__author__ = 'rdk'

from app import db


class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(64), index = True, unique = True)
    date = db.Column(db.DateTime)
    work_days = db.Column(db.Float)
    price_htva = db.Column(db.Float)
    price_total = db.Column(db.Float)
    daily_rate = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable = False)
    customer = db.relationship('Customer', backref=db.backref('invoices', cascade="all, delete-orphan"), lazy='joined')

    def __repr__(self):
        return '<Number %r>' % (self.number)