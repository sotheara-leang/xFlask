from injector import inject
from flask_sqlalchemy import SQLAlchemy


from xflask.dao import Dao

from main.model.user import User


class UserDao(Dao):


    @inject
    def __init__(self, db: SQLAlchemy):
        super(UserDao, self).__init__(User, db)

    def get_by_username(self, username):

        return self.filter(username=username)
