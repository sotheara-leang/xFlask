import logging
from injector import inject
from flask_jwt_extended import create_access_token

from xflask.service import CrudService
from xflask.exception import Exception
from xflask.type.sys_code import SysCode

from main.dao.user import UserDao
from main.type.biz_code import BizCode


class UserService(CrudService):

    _logger = logging.getLogger(__qualname__)

    @inject
    def __init__(self, dao: UserDao):
        super(UserService, self).__init__(dao)

    def create(self, obj):
        username = obj.username

        user = self.dao.get_by_username(username)
        if user is not None:
            self._logger.error('user existed: username=%s', username)
            raise Exception(SysCode.EXISTED)

        super().create(obj)

    def update(self, obj):
        user = obj.id
        if user is None:
            self._logger.error('user not found: id=%d', obj.id)
            raise Exception(SysCode.NOT_FOUND)

        username = obj.username
        if user.username == username and user.id != id:
            self._logger.error('username existed: id=%d, username=%', obj.id, username)
            raise Exception(BizCode.USER_NAME_EXISTED)

        super().update(obj)

    def auth(self, username, password):
        user = self.dao.get_by_username(username)
        if user is None:
            self._logger.error('user not found: username=%s', username)
            raise Exception(SysCode.NOT_FOUND)

        if user.password != password:
            self._logger.error('password invalid: username=%s, password=%s', username, password)
            raise Exception(BizCode.USER_PWD_INVALID)

        token = create_access_token(identity=user.serialize())
        return token
