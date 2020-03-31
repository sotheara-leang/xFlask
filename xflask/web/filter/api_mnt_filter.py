import logging

from flask import request

from xflask.exception import Exception
from xflask.type.sys_code import SysCode
from xflask.web.filter import Filter


class ApiMntFilter(Filter):

    def init(self, application):
        self._logger = logging.getLogger(self.__class__.__name__)

    def validate(self, route):
        return True

    def before(self):
        is_valid = self.validate(request.path)
        if is_valid is False:
            raise Exception(SysCode.API_NOT_AVAILABLE)
