#-*- coding: utf-8 -*-
__author__ = 'rdk'

from datetime import timedelta, datetime
from flask import jsonify, request
from app import app, db, CAL_FMT, DATE_FMT, TIME_FMT
from app.models import Presta, Project
from app.forms import PrestaFrom


class prestas_event(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


@app.route('/presta')
def get_prestas():
    # prestas = Presta.query.all()
    from_date = datetime.strptime(request.args.get('start', ''), CAL_FMT)
    to_date = datetime.strptime(request.args.get('end', ''), CAL_FMT)

    prestas = Presta.query.filter(Presta.date >= from_date, Presta.date <= to_date).all()
    lst_presta = []

    for p in prestas:
        # Properties matches the fullcalendar event properties
        lst_presta.append(
            prestas_event(id = p.id, title = Project.query.filter_by(id = p.project_id).first().code,
                          start = p.date, end = p.date + timedelta(seconds = p.duration), duration=p.duration)
        )

    return jsonify([ob.__dict__ for ob in lst_presta])


@app.route('/presta/add', methods=['POST'])
def add_presta():
    presta = PrestaFrom()
    presta.project.choices = [(p.id, p.code) for p in Project.query.all()]
    presta.id.data = 0

    if presta.validate_on_submit():
        new_presta = Presta()

        new_presta.project_id = presta.project.data
        new_presta.date = datetime.strptime(presta.date.data, DATE_FMT)
        duration = datetime.strptime(presta.duration.data.replace(' ', ''), TIME_FMT)
        new_presta.duration = timedelta(hours=duration.hour, minutes=duration.minute).seconds
        new_presta.description = presta.comment.data

        db.session.add(new_presta)
        db.session.commit()

        return jsonify(data={'message': 'Presta inserted'})

    print(presta.errors)
    return jsonify(data=presta.errors)


@app.route('/presta/update', methods=['POST'])
def update_presta():
    presta = PrestaFrom()
    presta.project.choices = [(p.id, p.code) for p in Project.query.all()]

    if presta.validate_on_submit():
        p = Presta.query.filter_by(id=presta.id.data).first()

        p.project_id = presta.project.data
        p.date = datetime.strptime(presta.date.data, DATE_FMT)
        duration = datetime.strptime(presta.duration.data.replace(' ', ''), TIME_FMT)
        p.duration = timedelta(hours=duration.hour, minutes=duration.minute).seconds
        p.description = presta.comment.data

        db.session.add(p)
        db.session.commit()

        print("update presta with id %d" % presta.id.data)
        return jsonify(data={'message': 'Presta updated'})

    print(presta.errors)
    return jsonify(data=presta.errors)


@app.route('/presta/delete', methods=['POST'])
def delete_presta():
    pobj = Presta.query.filter_by(id=int(request.json['prestaid'])).first()

    if pobj is not None:
        db.session.delete(pobj)
        db.session.commit()

    return jsonify(data={'message': 'Presta deleted'})


@app.route('/presta/detail', methods=['GET'])
def get_presta_detail():
    presta = Presta.query.filter_by(id=request.args.get('prestaid', 0, type=int)).first()

    if presta is not None:
        data = dict(Description=presta.description, Project=presta.project_id,
                    Duration=("%02d : %02d" % (presta.duration / 3600, presta.duration % 3600)))
        return jsonify(data)