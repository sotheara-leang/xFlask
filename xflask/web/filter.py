import logging

from flask import request
from werkzeug.routing import Map, Rule


class Filter(object):

    def init(self, application):
        pass

    def before(self):
        pass

    def after(self, response):
        return response


class ApiLoggingFilter(Filter):

    def init(self, application):
        self.logger = logging.getLogger(self.__class__.__name__)

    def __init__(self, routes=None, excludes=None):
        self.routes = routes or ['/api/<path:route>']
        self.excludes = excludes or ['/api/login']

        rules = []
        for route in self.routes:
            rules.append(Rule(route))

        self.matcher = Map(rules).bind('', '/')

        rules = []
        for route in self.excludes:
            rules.append(Rule(route))

        self.excludes_matcher = Map(rules).bind('', '/')

    def before(self):
        if self.routes is None or len(self.routes) == 0:
            return

        if self.excludes_matcher.test(request.path) is True:
            return

        if self.matcher.test(request.path) is True:
            self.logger.debug('>>> Request')
            self.logger.debug('%s %s\n' % (request.method, request.url))

            if request.is_json is True:
                try:
                    data = request.get_json()
                except Exception:
                    data = ''

                self.logger.debug(data)

    def after(self, response):
        if self.excludes_matcher.test(request.path) is True:
            return response

        if response.is_json is True:
            self.logger.debug('<<< Response')
            self.logger.debug(response.get_json())

        return response
