import logging

from flask import request
from werkzeug.routing import Map, Rule
from werkzeug.datastructures import CombinedMultiDict


class Filter(object):
    order = None

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
            self.logger.debug('%s %s' % (request.method, request.url))

            headers = dict() if request.headers is None else dict(request.headers)
            content = request.get_json() if request.is_json else \
                CombinedMultiDict((request.files, request.form)).to_dict()

            self.logger.debug('Headers: %s' % headers)
            self.logger.debug('Data: %s' % content)

    def after(self, response):
        if self.excludes_matcher.test(request.path) is True:
            return response

        self.logger.debug('<<< Response')

        headers = dict() if response.headers is None else dict(response.headers)
        content = response.get_json()
        
        self.logger.debug('Headers: %s' % headers)
        self.logger.debug('Data: %s' % content)

        return response
