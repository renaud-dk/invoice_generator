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
    bank_account = db.Column(db.String(64))
    bank_swift = db.Column(db.String(64))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable = False)
    notification_id = db.Column(db.Integer, db.ForeignKey('notification.id'), nullable=True)
    customer = db.relationship('Customer', backref=db.backref('invoices', cascade="all, delete-orphan"), lazy='joined')
    notification = db.relationship('Notification', backref=db.backref('invoices', cascade="all, delete-orphan"), lazy='joined')

    def __repr__(self):
        return '<Number %r>' % (self.number)