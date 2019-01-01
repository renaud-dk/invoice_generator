# -*- coding: utf-8 -*-
__author__ = 'rdk'

from app import db


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    notification = db.Column(db.Text, nullable=False)
    date_from = db.Column(db.DateTime, nullable=False)
    date_to = db.Column(db.DateTime, nullable=False)
