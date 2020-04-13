# -*- coding: utf-8 -*-

from .auth import SignupApi, LoginApi

def initialize_routes(api):
    api.add_resource(SignupApi, '/api/v1/auth/signup')
    api.add_resource(LoginApi, '/api/v1/auth/login')