import logging
from injector import inject
from flask_jwt_extended import create_access_token

from xflask.service import Service
from xflask.exception import Exception

from main.dao.user import UserDao
from main.type.biz_code import BizCode


class UserService(Service):

    _logger = logging.getLogger(__qualname__)

    @inject
    def __init__(self, dao: UserDao):
        super(UserService, self).__init__(dao)

    def get_by_username(self, username):
        return self.dao.get_by_username(username)

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
