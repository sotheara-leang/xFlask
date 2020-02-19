import logging
from flask import render_template
from flask import request
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import NotFound, BadRequest, MethodNotAllowed

from xflask.exception import Exception as Sys_Exception
from xflask.type.sys_code import SysCode
from xflask.web.response import Response


class ErrorHandler(object):

    def init(self, server):
        pass

    def handler_404(self, e):
        pass

    def handler_400(self, e):
        pass

    def handler_500(self, e):
        pass


class SimpleErrorHandler(ErrorHandler):
    DEF_API_ROUTE = '/api'
    DEF_TEMPLATE = ''

    def __init__(self, api_route=DEF_API_ROUTE, template=DEF_TEMPLATE):
        self.api_route = api_route
        self.template = template

    def init(self, server):
        self.logger = logging.getLogger(self.__class__.__name__)

        server.app.register_error_handler(NotFound, self.handler_404)
        server.app.register_error_handler(BadRequest, self.handler_400)
        server.app.register_error_handler(MethodNotAllowed, self.handler_400)
        server.app.register_error_handler(ValidationError, self.handler_400)
        server.app.register_error_handler(Exception, self.handler_500)

    def handler_404(self, e):
        self.logger.exception('404 error')

        if request.path.startswith(self.api_route):
            return Response.fail(SysCode.NOT_FOUND).to_dict()
        else:
            return render_template(self.template + '404.html')

    def handler_400(self, e):
        self.logger.exception('400 error')

        if request.path.startswith(self.api_route):
            if isinstance(e, ValidationError):
                return Response.fail(SysCode.INVALID, e.messages).to_dict()
            else:
                return Response.fail(SysCode.INVALID).to_dict()
        else:
            return render_template(self.template + '400.html')

    def handler_500(self, e):
        self.logger.exception('500 error')

        if request.path.startswith(self.api_route):
            code = e.code if isinstance(e, Sys_Exception) else SysCode.SYS_ERROR
            return Response.fail(code).to_dict()
        else:
            return render_template(self.template + '500.html')

