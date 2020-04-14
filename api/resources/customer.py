# -*- coding: utf-8 -*-

import datetime
import json

from flask import request, Response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

from api.app import db
from api.database.user import User
from api.database.customer import Customer
# from api.resources.errors import EmailAlreadyExistsError, \
#     UnauthorizedError, InternalServerError


class CustomersApi(Resource):
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        
        customers = []
        cust = Customer.query \
                .join(User) \
                .filter(User.id == user_id).all()

        for c in cust:
            customers.append(c.as_dict())
        
        return Response(json.dumps(customers), mimetype="application/json", status=200)

    @jwt_required
    def post(self):
        body = request.get_json()
        user_id = get_jwt_identity()

        cust = Customer(**body)
        cust.user_id = user_id

        db.session.add(cust)
        db.session.commit()
        return None, 200
