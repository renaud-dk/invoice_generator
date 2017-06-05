#-*- coding: utf-8 -*-
__author__ = 'rdk'

from flask import render_template
from app import app
from app.models import Project
from app.forms import PrestaFrom


@app.route('/', methods=['GET'])
@app.route('/index',  methods=['GET'])
def index():
    presta = PrestaFrom()
    presta.project.choices = [(p.id, p.code) for p in Project.query.all()]

    # Initialize id in case of insert
    presta.id.data = 0

    return render_template('index.html', presta=presta)

