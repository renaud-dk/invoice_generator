#-*- coding: utf-8 -*-
__author__ = 'rdk'

from app import db


class Presta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    duration = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    project = db.relationship('Project', backref=db.backref('prestas', cascade="all, delete-orphan"), lazy='joined')

    def __repr__(self):
        return '<Presta %r>' % (self.description)
