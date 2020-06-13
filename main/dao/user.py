from xflask.dao import Dao

from main.model.user import User


class UserDao(Dao):

    def __init__(self):
        super(UserDao, self).__init__(User)

    def get_by_username(self, username):
        return self.get_by_filter(username=username)

