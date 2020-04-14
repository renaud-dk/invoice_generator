# -*- coding: utf-8 -*-

__all__ = ["user", "customer", "presta"]

from .user import User
from .customer import Customer
from .project import Project
from .presta import Presta

def db_initialize(db):
    db.create_all()
