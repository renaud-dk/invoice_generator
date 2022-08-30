# -*- coding: utf-8 -*-

import datetime
import json

from flask import request, Response
from flask_jwt_extended import create_access_token
from flask_restful import Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

from api.app import db
from api.database.user import User
from api.resources.errors import EmailAlreadyExistsError, \
    UnauthorizedError, InternalServerError

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


class LoginApi(Resource):
    def post(self):
        try:
            body = request.get_json()
            user = User.query.filter_by(email=body.get('email')).first()
            authorized = user.check_password(body.get('password'))

            if not authorized:
                raise UnauthorizedError

            expires = datetime.timedelta(days=7)
            access_token = create_access_token(identity=str(user.id), expires_delta=expires)
            return {'token': access_token}, 200
            
        except (AttributeError, UnauthorizedError):
            raise UnauthorizedError
        except Exception as e:
            raise InternalServerError
