#-*- coding: utf-8 -*-
__author__ = 'rdk'

from app import db


class Refvalue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    refname = db.Column(db.String(64), index=True, unique=True, nullable=False)
    refvalue = db.Column(db.String(64))

    def __repr__(self):
        return '<Refvalue %r - %r>' % (self.refname, self.refvalue)
