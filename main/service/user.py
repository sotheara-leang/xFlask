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
    logger = logging.getLogger(__qualname__)

    @inject
    def __init__(self, dao: UserDao):
        super(UserService, self).__init__(dao)

    def get_page(self, page, sort=None, criterion=None):
        # sort
        sort_ = []
        if sort is not None:
            for e in sort:
                sort_.append(User.get_sort_expression(e.field, e.order))

        # criterion
        criterion_ = {}
        if criterion is not None:
            if criterion.username is not None and criterion.username != '':
                criterion_['username'] = User.username.like('%{}$'.format(criterion.username))

            if criterion.edu_level is not None:
                criterion_['edu_level'] = criterion.edu_level

            if criterion.role_id is not None:
                criterion_['role_id'] = criterion.role_id

        pagination = self.dao.get_page(page.page, page.per_page, tuple(sort_), **criterion_)
        return pagination

    def create_user(self, obj):
        username = obj.username

        user = self.dao.get_by_username(username)
        if user is not None:
            self.logger.error('user existed: username=%s', username)
            raise Exception(SysCode.EXISTED)

        self.create(obj)

    def update_user(self, obj):
        user = self.dao.get(obj.id)
        if user is None:
            self.logger.error('user not found: id=%d', obj.id)
            raise Exception(SysCode.NOT_FOUND)

        username = obj.username
        if user.username == username and user.id != obj.id:
            self.logger.error('username existed: id=%d, username=%', obj.id, username)
            raise Exception(BizCode.USER_NAME_EXISTED)

        self.update(obj)

    def auth_user(self, username, password):
        user = self.dao.get_by_username(username)
        if user is None:
            self.logger.error('user not found: username=%s', username)
            raise Exception(SysCode.NOT_FOUND)

        if user.password != password:
            self.logger.error('password invalid: username=%s, password=%s', username, password)
            raise Exception(BizCode.USER_PWD_INVALID)

        token = create_access_token(identity=user.to_dict())
        return token
