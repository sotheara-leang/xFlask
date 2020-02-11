from flask import request
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended.exceptions import *
from werkzeug.routing import Map, Rule

from xflask.exception import Exception
from xflask.type.status_code import *


class Filter(object):

    def init(self, server):
        pass

    def before(self):
        pass

    def after(self, response):
        return response


class AuthTokenFilter(Filter):

    def __init__(self, open_routes=None):
        self.open_routes = open_routes or ['/api/login', '/static/*']

        rules = []
        for route in self.open_routes:
            rules.append(Rule(route))

        self.matcher = Map(rules).bind('', '/')

    def init(self, server):
        server.app.before_request(self.before)
        server.app.after_request(self.after)

    def before(self):
        if self.open_routes is None or len(self.open_routes) == 0:
            return

        if self.matcher.test(request.path) is False:
            try:
                verify_jwt_in_request()
            except JWTExtendedException:
                raise Exception(SC_AUTH_INVALID)
