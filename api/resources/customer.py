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
from api.resources.errors import EmailAlreadyExistsError, \
    UnauthorizedError, InternalServerError, NotFound


class CustomersApi(Resource):
    @jwt_required()
    def get(self):
        try:
            user_id = get_jwt_identity()
            
            customers = []
            cust = Customer.query \
                    .join(User) \
                    .filter(User.id == user_id).all()

            for c in cust:
                customers.append(c.as_dict())
            
            return Response(json.dumps(customers), mimetype="application/json", status=200)
        except NoAuthorizationError:
            raise UnauthorizedError
        except Exception as e:
            raise InternalServerError

    @jwt_required()
    def post(self):
        try:
            body = request.get_json()
            user_id = get_jwt_identity()

            cust = Customer(**body)
            cust.user_id = user_id

            db.session.add(cust)
            db.session.commit()
            return None, 200
        except NoAuthorizationError:
            raise UnauthorizedError
        except Exception as e:
            raise InternalServerError
        finally:
            db.session.rollback()


class CustomerApi(Resource):
    @jwt_required()
    def get(self, id):
        try:
            user_id = get_jwt_identity()

            customer = Customer.query \
                        .join(User) \
                        .filter(User.id == user_id) \
                        .filter(Customer.id == id).first()

            if customer is None:
                raise NotFound

            return Response(json.dumps(customer.as_dict()), mimetype="application/json", status=200)
        except NotFound:
            raise NotFound
        except Exception as e:
            raise InternalServerError

    @jwt_required
    def put(self, id):
        try:
            body = request.get_json()
            user_id = get_jwt_identity()

            customer = Customer.query \
                        .join(User) \
                        .filter(User.id == user_id) \
                        .filter(Customer.id == id).first()

            if customer is None:
                raise NotFound

            for key, value in body.items():
                setattr(customer, key, value)

            db.session.commit()
            return None, 200
        except NotFound:
            raise NotFound
        except Exception as e:
            raise InternalServerError
        finally:
            db.session.rollback()

    @jwt_required
    def delete(self, id):
        try:
            user_id = get_jwt_identity()

            customer = Customer.query \
                        .join(User) \
                        .filter(User.id == user_id) \
                        .filter(Customer.id == id).first()

            if customer is None:
                raise NotFound

            db.session.delete(customer)
            db.session.commit()
            return None, 200
        except NotFound:
            raise NotFound
        except Exception as e:
            raise InternalServerError
        finally:
            db.session.rollback()
