# -*- coding: utf-8 -*-

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from api.resources.errors import errors

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "invoice_generator.db"))

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = 't1NP63m4wnBg6nyHYKfmc2TpCOGI4nss'

# Create api
api = Api(app, errors=errors)

# Initialize bcrypt
bcrypt = Bcrypt(app)

# Initialize JWT
jwt = JWTManager(app)

# Create database
db = SQLAlchemy(app)

# Initialize database done in the database module so table are populated.
from api.database import db_initialize
db_initialize(db)

# Initialize routes
from api.resources.routes import initialize_routes
initialize_routes(api)
