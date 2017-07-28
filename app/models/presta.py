#-*- coding: utf-8 -*-
__author__ = 'rdk'

from app import db


class Presta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    duration = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    travel_distance = db.Column(db.Integer, default=0, server_default='INTEGER DEFAULT 0')
    travel_comment = db.Column(db.Text, nullable=True)
    invoice_number = db.Column(db.String(64), nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    project = db.relationship('Project', backref=db.backref('prestas', cascade="all, delete-orphan"), lazy='joined')

    def __repr__(self):
        return '<Presta %r>' % (self.description)
