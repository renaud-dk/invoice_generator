#-*- coding: utf-8 -*-
__author__ = 'rdk'

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

# Some constant used across the application
REF_INVOICE_NUMBER = "INVOICE_NUMBER"
REF_BANK_ACCOUNT = "BANK_ACCOUNT"
REF_BANK_SWIFT = "BANK_SWIFT"

DATE_FMT='%d/%m/%Y %H:%M'
TIME_FMT='%H:%M'
CAL_FMT= '%Y-%m-%d'

FILE_TYPE_PRJ = 1
FILE_TYPE_PST = 2

REPORT_TYPE_HOLIDAYS = 1
REPORT_TYPE_TRAVELS = 2
REPORT_TYPE_PRESTAS = 3

# from app import views, models
from app.views import *
from app.models import *
