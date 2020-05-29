import logging

from flask import render_template
from flask import request
from werkzeug.exceptions import NotFound, BadRequest, MethodNotAllowed

from xflask.common.util import to_dict
from xflask.exception import Exception as Sys_Exception
from xflask.type.sys_code import SysCode
from xflask.web.response import Response


class ErrorHandler(object):

    def init(self, application):
        pass

    def handle_404(self, e):
        pass

    def handle_400(self, e):
        pass

    def handle_500(self, e):
        pass


class SimpleErrorHandler(ErrorHandler):
    DEF_API_ROUTE = '/api'
    DEF_TEMPLATE_FOLDER = ''

    def __init__(self, api_route=DEF_API_ROUTE, template_folder=DEF_TEMPLATE_FOLDER):
        self.api_route = api_route
        self.template_folder = template_folder

    def init(self, application):
        self.logger = logging.getLogger(self.__class__.__name__)

        application.app.register_error_handler(NotFound, self.handle_404)
        application.app.register_error_handler(BadRequest, self.handle_400)
        application.app.register_error_handler(MethodNotAllowed, self.handle_400)
        application.app.register_error_handler(Exception, self.handle_500)

    def handle_404(self, e):
        self.logger.exception('404 error')

        if request.path.startswith(self.api_route):
            return to_dict(Response.fail(SysCode.NOT_FOUND))
        else:
            return render_template(self.template_folder + '404.html')

    def handle_400(self, e):
        self.logger.exception('400 error')

        if request.path.startswith(self.api_route):
            return to_dict(Response.fail(SysCode.INVALID))
        else:
            return render_template(self.template_folder + '400.html')

    def handle_500(self, e):
        self.logger.exception('500 error')

        if request.path.startswith(self.api_route):
            if isinstance(e, Sys_Exception):
                response = Response.fail(e.code, e.data)
            else:
                response = Response.fail(SysCode.SYS_ERROR)

            return to_dict(response)
        else:
            data = None
            if isinstance(e, Sys_Exception):
                data = e.data

            return render_template(self.template_folder + '500.html', errors=data)
