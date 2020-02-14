import logging
from injector import inject
from flask_jwt_extended import create_access_token

from xflask.service import Service
from xflask.exception import Exception

from main.dao.user import UserDao
from main.model.user import User
from main.type.biz_code import *


class UserService(Service):

    logger = logging.getLogger(__qualname__)

    @inject
    def __init__(self, user_dao: UserDao):
        self.user_dao = user_dao

    def get_users(self):
        return self.user_dao.get_users()

    def get_user(self, user_id):
        return self.user_dao.get_user(user_id)

    def get_user_by_username(self, username):
        return self.user_dao.get_user_by_username(username)

    def create_user(self, user: User):
        self.user_dao.create_user(user)

    def auth(self, username, password):
        user = self.user_dao.get_user_by_username(username)
        if user is None:
            self.logger.error('user not found: username=%s', username)
            raise Exception(BC_USER_NOT_FOUND)

        if user.password != password:
            self.logger.error('password invalid: username=%s, password=%s', username, password)
            raise Exception(BC_PWD_INVALID)

        token = create_access_token(identity=user.to_dict())
        return token
