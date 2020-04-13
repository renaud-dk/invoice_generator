# -*- coding: utf-8 -*-

import datetime

from flask import request, Response
from flask_jwt_extended import create_access_token
from flask_restful import Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

from api.app import db
from api.database.user import User
from api.resources.errors import EmailAlreadyExistsError

class SignupApi(Resource):
    def post(self):
        try:
            body = request.get_json()
            usr = User(**body)
            usr.hash_password()
            db.session.add(usr)
            db.session.commit()
            return None, 200
        except IntegrityError:
            raise EmailAlreadyExistsError
        finally:
            db.session.rollback()