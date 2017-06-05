#-*- coding: utf-8 -*-
__author__ = 'rdk'

import os

# Databese configurtation
basedir = os.path.abspath(os.path.dirname(__file__))
dbdir = os.path.join(basedir, 'database') 

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(dbdir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(dbdir, 'db_repository')

# Explicit set tracking modification to enable migration
SQLALCHEMY_TRACK_MODIFICATIONS = True

# Flask-WTF configuration
WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

# Upload configuration
UPLOAD_FOLDER = '/tmp/invoice-generator/uploads'
ALLOWED_EXTENSIONS = set(['csv'])
