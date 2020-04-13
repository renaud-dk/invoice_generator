# -*- coding: utf-8 -*-

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from api.resources.errors import errors

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "invoice_generator.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["JWT_SECRET_KEY"] = 't1NP63m4wnBg6nyHYKfmc2TpCOGI4nss'

# Create api
api = Api(app, errors=errors)

# Initialize bcrypt
bcrypt = Bcrypt(app)

# Initialize JWT
jwt = JWTManager(app)

# Create database
db = SQLAlchemy(app)

# This is needed to create the database and all the tables
# from api.database import *
# db.create_all()

# $2b$12$6cqn5YSfwbIHsxbA89AAcek/SgMp9aOvRHcQMBsEZLD85MMxlGkWe  

from api.database import db_initialize
db_initialize(db)

from api.resources.routes import initialize_routes
initialize_routes(api)

# from api.database.user import User

# usr_data = {"email":"renaud.dk@gmail.com", "password":"123456"}
# usr = User(**usr_data)
# usr.hash_password()
# db.session.add(usr)
# try:
#     db.session.commit()
# except Exception as e:
#     db.session.rollback()

