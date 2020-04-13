# -*- coding: utf-8 -*-

from .auth import SignupApi

def initialize_routes(api):
    api.add_resource(SignupApi, '/api/v1/auth/signup')