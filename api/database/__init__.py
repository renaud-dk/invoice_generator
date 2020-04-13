# -*- coding: utf-8 -*-

__all__ = ["user"]

from .user import User

def db_initialize(db):
    db.create_all()