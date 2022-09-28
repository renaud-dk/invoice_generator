# -*- coding: utf-8 -*-

import datetime
import json

from flask import request, Response, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended.exceptions import NoAuthorizationError


from api.app import db
from api.database.user import User
from api.database.customer import Customer
from api.database.project import Project
from api.resources.errors import UnauthorizedError, InternalServerError, NotFound
from api.schema import project_schema


class ProjectsApi(Resource):
    @jwt_required()
    def get(self):
        try:
            user_id = get_jwt_identity()
            
            prj = Project.query \
                    .join(Customer) \
                    .join(User) \
                    .filter(User.id == user_id).all()

            if prj is None:
                raise NotFound

            return jsonify(project_schema.dump(prj, many=True))
        except NoAuthorizationError:
            raise UnauthorizedError
        except NotFound:
            raise NotFound
        except Exception as e:
            raise InternalServerError

class ProjectApi(Resource):
    @jwt_required()
    def get(self, id):
        try:
            user_id = get_jwt_identity()

            prj = Project.query \
                        .join(Customer) \
                        .join(User) \
                        .filter(User.id == user_id) \
                        .filter(Project.id == id).first()

            if prj is None:
                raise NotFound

            return jsonify(project_schema.dump(prj))

        except NoAuthorizationError:
            raise UnauthorizedError
        except NotFound:
            raise NotFound
        except Exception as e:
            raise InternalServerError   

    @jwt_required()
    def put(self, id):
        try:
            user_id = get_jwt_identity()
            body = request.get_json()

            prj = Project.query \
                        .join(Customer) \
                        .join(User) \
                        .filter(User.id == user_id) \
                        .filter(Project.id == id).first()

            if prj is None:
                raise NotFound

            for key, value in body.items():
                setattr(prj, key, value)

            db.session.commit()

            return None, 200

        except NoAuthorizationError:
            raise UnauthorizedError
        except NotFound:
            raise NotFound
        except Exception as e:
            raise InternalServerError


class ProjectsCustomerApi(Resource):
    @jwt_required()
    def get(self, cust_id):
        try:
            user_id = get_jwt_identity()

            projects = []
            prj = Project.query \
                    .join(Customer) \
                    .join(User) \
                    .filter(User.id == user_id) \
                    .filter(Customer.id == cust_id).all()

            if prj is None:
                raise NotFound

            for p in prj:
                projects.append(p.as_dict())
            
            return Response(json.dumps(projects), mimetype="application/json", status=200)
        except NotFound:
            raise NotFound
        except Exception as e:
            raise InternalServerError

    @jwt_required()
    def post(self, cust_id):
        try:
            user_id = get_jwt_identity()
            body = request.get_json()
            project = Project(**body)
            
            customer = Customer.query \
                    .join(User) \
                    .filter(User.id == user_id) \
                    .filter(Customer.id == cust_id).first()

            customer.projects.append(project)

            db.session.add(customer)
            db.session.add(project)
            db.session.commit()

            return None, 200
        except Exception as e:
            raise InternalServerError
        finally:
            db.session.rollback()


class ProjectCustomerApi(Resource):    
    @jwt_required()
    def get(self, cust_id, prj_id):
        try:
            user_id = get_jwt_identity()

            project = Project.query \
                        .join(Customer) \
                        .join(User) \
                        .filter(User.id == user_id) \
                        .filter(Customer.id == cust_id) \
                        .filter(Project.id == prj_id).first()

            if project is None:
                raise NotFound

            return Response(json.dumps(project.as_dict()), mimetype="application/json", status=200)
        except NotFound:
            raise NotFound
        except Exception as e:
            raise InternalServerError

    @jwt_required()
    def put(self, cust_id, prj_id):
        try:
            user_id = get_jwt_identity()
            body = request.get_json()

            project = Project.query \
                        .join(Customer) \
                        .join(User) \
                        .filter(User.id == user_id) \
                        .filter(Customer.id == cust_id) \
                        .filter(Project.id == prj_id).first()

            if project is None:
                raise NotFound

            for key, value in body.items():
                setattr(project, key, value)

            db.session.commit()

            return None, 200
        except NotFound:
            raise NotFound
        except Exception as e:
            raise InternalServerError

    @jwt_required()
    def delete(self, cust_id, prj_id):
        try:
            user_id = get_jwt_identity()

            project = Project.query \
                        .join(Customer) \
                        .join(User) \
                        .filter(User.id == user_id) \
                        .filter(Customer.id == cust_id) \
                        .filter(Project.id == prj_id).first()

            if project is None:
                raise NotFound

            db.session.delete(project)
            db.session.commit()

            return None, 200
        except NotFound:
            raise NotFound
        except Exception as e:
            raise InternalServerError
