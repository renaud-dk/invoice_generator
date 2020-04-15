# -*- coding: utf-8 -*-

from .auth import SignupApi, LoginApi
from .customer import CustomersApi, CustomerApi
from .project import ProjectsApi, ProjectsCustomerApi, ProjectCustomerApi
from .presta import PrestasApi, PrestasProjectApi, PrestaProjectApi

def initialize_routes(api):
    api.add_resource(SignupApi, '/api/v1/auth/signup')
    api.add_resource(LoginApi, '/api/v1/auth/login')
    api.add_resource(CustomersApi, '/api/v1/customers')
    api.add_resource(CustomerApi, '/api/v1/customers/<id>')
    api.add_resource(ProjectsApi, '/api/v1/projects')
    api.add_resource(ProjectsCustomerApi, '/api/v1/customers/<cust_id>/projects')
    api.add_resource(ProjectCustomerApi, '/api/v1/customers/<cust_id>/projects/<prj_id>')
    api.add_resource(PrestasApi, '/api/v1/prestas')
    api.add_resource(PrestasProjectApi, '/api/v1/customers/<cust_id>/projects/<prj_id>/prestas')
    api.add_resource(PrestaProjectApi, '/api/v1/customers/<cust_id>/projects/<prj_id>/prestas/<prst_id>')
