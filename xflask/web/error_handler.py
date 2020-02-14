from flask import render_template
from flask import request
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import NotFound, BadRequest, MethodNotAllowed

from xflask.exception import Exception
from xflask.type.status_code import StatusCode
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
        server.app.register_error_handler(NotFound, self.handler_404)
        server.app.register_error_handler(BadRequest, self.handler_400)
        server.app.register_error_handler(MethodNotAllowed, self.handler_400)
        server.app.register_error_handler(ValidationError, self.handler_400)
        server.app.register_error_handler(Exception, self.handler_500)

    def handler_404(self, e):
        if request.path.startswith(self.api_route):
            return Response.fail(StatusCode.NOT_FOUND).to_dict()
        else:
            return render_template(self.template + '404.html')

    def handler_400(self, e):
        if request.path.startswith(self.api_route):
            if isinstance(e, ValidationError):
                return Response(StatusCode.INVALID, e.messages).to_dict()
            else:
                return Response.fail(StatusCode.INVALID).to_dict()
        else:
            return render_template(self.template + '400.html')

    def handler_500(self, e):
        if request.path.startswith(self.api_route):
            code = e.code if isinstance(e, Exception) else StatusCode.SYS_ERROR
            return Response.fail(code).to_dict()
        else:
            return render_template(self.template + '500.html')
