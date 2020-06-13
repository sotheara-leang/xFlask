import logging

from flask_jwt_extended import create_access_token
from injector import inject

from main.dao.user import UserDao
from main.model.user import User
from main.type.biz_code import BizCode
from xflask.exception import Exception
from xflask.service import CrudService
from xflask.type.sys_code import SysCode


class UserService(CrudService):
    _logger = logging.getLogger(__qualname__)

    @inject
    def __init__(self, dao: UserDao):
        super(UserService, self).__init__(dao)

    def get_page_by_filter(self, page, per_page, sort=[], filter=None):
        # sort
        sort_ = []
        for e in sort:
            sort_.append(User.get_sort_expression(e.field, e.order))

        # filter
        filter_ = {}
        if filter is not None:
            if filter.username is not None and filter.username != '':
                filter_['username'] = User.username.like('%{}$'.format(filter.username))

            if filter.edu_level is not None:
                filter_['edu_level'] = filter.edu_level

            if filter.role_id is not None:
                filter_['role_id'] = filter.role_id

        pagination = self.dao.get_page_by_filter(page, per_page, tuple(sort_), **filter_)
        return pagination

    def create(self, obj):
        username = obj.username

        user = self.dao.get_by_username(username)
        if user is not None:
            self._logger.error('user existed: username=%s', username)
            raise Exception(SysCode.EXISTED)

        self.dao.insert(obj)

    def update(self, obj):
        user = self.dao.get(obj.id)
        if user is None:
            self._logger.error('user not found: id=%d', obj.id)
            raise Exception(SysCode.NOT_FOUND)

        username = obj.username
        if user.username == username and user.id != obj.id:
            self._logger.error('username existed: id=%d, username=%', obj.id, username)
            raise Exception(BizCode.USER_NAME_EXISTED)

        self.dao.update(obj)

    def auth(self, username, password):
        user = self.dao.get_by_username(username)
        if user is None:
            self._logger.error('user not found: username=%s', username)
            raise Exception(SysCode.NOT_FOUND)

        if user.password != password:
            self._logger.error('password invalid: username=%s, password=%s', username, password)
            raise Exception(BizCode.USER_PWD_INVALID)

        token = create_access_token(identity=user.to_dict())
        return token
