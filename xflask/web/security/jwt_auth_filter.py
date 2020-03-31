from flask import request
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended.exceptions import *
from werkzeug.routing import Map, Rule

from xflask.exception import Exception
from xflask.type.sys_code import SysCode
from xflask.web.filter import Filter


class JwtAuthFilter(Filter):

    def __init__(self, open_routes=None):
        self.open_routes = open_routes or ['/api/login', '/static/<path:route>']

        rules = []
        for route in self.open_routes:
            rules.append(Rule(route))

        self.matcher = Map(rules).bind('', '/')

    def before(self):
        if self.open_routes is None or len(self.open_routes) == 0:
            return

        if self.matcher.test(request.path) is False:
            try:
                verify_jwt_in_request()
            except JWTExtendedException:
                raise Exception(SysCode.AUTH_INVALID)
