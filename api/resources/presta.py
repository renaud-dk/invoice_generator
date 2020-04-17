# -*- coding: utf-8 -*-

import datetime
import json

from flask import request, Response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended.exceptions import NoAuthorizationError
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

from api.app import db
from api.database.user import User
from api.database.customer import Customer
from api.database.project import Project
from api.database.presta import Presta
from api.resources.errors import EmailAlreadyExistsError, \
    UnauthorizedError, InternalServerError, NotFound

def json_converter(o):
    if isinstance(o, datetime.datetime):
        return o.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

begin_of_all = '1970-01-01T00:00:00.000Z'
end_of_all = '3000-01-01T00:00:00.000Z'

class PrestasApi(Resource):
    @jwt_required
    def get(self):
        try:
            user_id = get_jwt_identity()
            start = datetime.datetime.strptime(request.args.get('start', begin_of_all),'%Y-%m-%dT%H:%M:%S.%fZ') 
            end = datetime.datetime.strptime(request.args.get('end', end_of_all),'%Y-%m-%dT%H:%M:%S.%fZ') 

            print(f"start : {start} - {type(start)}")
            print(f"end : {end} - {type(end)}")
            
            prestas = []
            prst = Presta.query \
                    .join(Project) \
                    .join(Customer) \
                    .join(User) \
                    .filter(User.id == user_id) \
                    .filter(Presta.date >= start, Presta.date <= end).all()

            if prst is None:
                raise NotFound

            for p in prst:
                prestas.append(p.as_dict())
            
            return Response(json.dumps(prestas, default=json_converter), mimetype="application/json", status=200)
        except NoAuthorizationError:
            raise UnauthorizedError
        except NotFound:
            raise NotFound
        except Exception as e:
            raise InternalServerError


class PrestasProjectApi(Resource):
    @jwt_required
    def get(self, cust_id, prj_id):
        try:
            user_id = get_jwt_identity()

            prestas = []
            prst = Presta.query \
                    .join(Project) \
                    .join(Customer) \
                    .join(User) \
                    .filter(User.id == user_id) \
                    .filter(Customer.id == cust_id) \
                    .filter(Project.id == prj_id).all()

            if prst is None:
                raise NotFound

            for p in prst:
                prestas.append(p.as_dict())
            
            return Response(json.dumps(prestas), mimetype="application/json", status=200)
        except NotFound:
            raise NotFound
        except Exception as e:
            raise InternalServerError

    @jwt_required
    def post(self, cust_id, prj_id):
        try:
            user_id = get_jwt_identity()
            body = request.get_json()
            presta = Presta(**body)

            presta.date = datetime.datetime.strptime(presta.date, '%Y-%m-%dT%H:%M:%S.%fZ')
            
            project = Project.query \
                    .join(Customer) \
                    .join(User) \
                    .filter(User.id == user_id) \
                    .filter(Customer.id == cust_id) \
                    .filter(Project.id == prj_id).first()

            project.prestas.append(presta)

            db.session.add(project)
            db.session.add(presta)
            db.session.commit()

            return None, 200
        except Exception as e:
            raise InternalServerError
        finally:
            db.session.rollback()


class PrestaProjectApi(Resource):    
    @jwt_required
    def get(self, cust_id, prj_id, prst_id):
        try:
            user_id = get_jwt_identity()

            presta = Presta.query \
                        .join(Project) \
                        .join(Customer) \
                        .join(User) \
                        .filter(User.id == user_id) \
                        .filter(Customer.id == cust_id) \
                        .filter(Project.id == prj_id) \
                        .filter(Presta.id == prst_id).first()

            if presta is None:
                raise NotFound

            return Response(json.dumps(presta.as_dict(), default=json_converter), mimetype="application/json", status=200)
        except NotFound:
            raise NotFound
        except Exception as e:
            raise InternalServerError

    @jwt_required
    def put(self, cust_id, prj_id, prst_id):
        try:
            user_id = get_jwt_identity()
            body = request.get_json()

            presta = Presta.query \
                        .join(Project) \
                        .join(Customer) \
                        .join(User) \
                        .filter(User.id == user_id) \
                        .filter(Customer.id == cust_id) \
                        .filter(Project.id == prj_id) \
                        .filter(Presta.id == prst_id).first()

            if presta is None:
                raise NotFound

            for key, value in body.items():
                setattr(presta, key, value)

            presta.date = datetime.datetime.strptime(presta.date, '%Y-%m-%dT%H:%M:%S.%fZ')

            db.session.commit()

            return None, 200
        except NotFound:
            raise NotFound
        except Exception as e:
            raise InternalServerError

    @jwt_required
    def delete(self, cust_id, prj_id, prst_id):
        try:
            user_id = get_jwt_identity()

            presta = Presta.query \
                        .join(Project) \
                        .join(Customer) \
                        .join(User) \
                        .filter(User.id == user_id) \
                        .filter(Customer.id == cust_id) \
                        .filter(Project.id == prj_id) \
                        .filter(Presta.id == prst_id).first()

            if presta is None:
                raise NotFound

            db.session.delete(presta)
            db.session.commit()

            return None, 200
        except NotFound:
            raise NotFound
        except Exception as e:
            raise InternalServerError
