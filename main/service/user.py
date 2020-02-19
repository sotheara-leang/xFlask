import logging
from injector import inject
from flask_jwt_extended import create_access_token

from xflask.common.obj_util import get_attr
from xflask.service import CrudService
from xflask.exception import Exception
from xflask.type.status_code import StatusCode

from main.dao.user import UserDao
from main.type.biz_code import BizCode


class UserService(CrudService):

    _logger = logging.getLogger(__qualname__)

    @inject
    def __init__(self, dao: UserDao):
        super(UserService, self).__init__(dao)

    def create(self, obj):
        username = get_attr(obj, 'username')

        user = self.dao.get_by_username(username)
        if user is not None:
            self._logger.error('user existed: username=%s', username)
            raise Exception(StatusCode.EXISTED)

        super().create(obj)

    def update(self, obj):
        id = get_attr(obj, 'id')

        user = self.get(id)
        if user is None:
            self._logger.error('user not found: id=%d', id)
            raise Exception(StatusCode.NOT_FOUND)

        username = get_attr(obj, 'username')
        if user.username != username and user.id != id:
            self._logger.error('username existed: id=%d, username=%', id, username)
            raise Exception(StatusCode.EXISTED)

        super().update(obj)

    def auth(self, username, password):
        user = self.dao.get_by_username(username)
        if user is None:
            self._logger.error('user not found: username=%s', username)
            raise Exception(BizCode.USER_NOT_FOUND)

        if user.password != password:
            self._logger.error('password invalid: username=%s, password=%s', username, password)
            raise Exception(BizCode.PWD_INVALID)

        token = create_access_token(identity=user.to_dict())
        return token
