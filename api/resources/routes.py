# -*- coding: utf-8 -*-

from .auth import SignupApi, LoginApi
from .customer import CustomersApi

def initialize_routes(api):
    api.add_resource(SignupApi, '/api/v1/auth/signup')
    api.add_resource(LoginApi, '/api/v1/auth/login')
    api.add_resource(CustomersApi, '/api/v1/customers')
