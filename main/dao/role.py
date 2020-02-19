from injector import inject
from flask_sqlalchemy import SQLAlchemy

from xflask.dao import Dao

from main.model.role import Role


class RoleDao(Dao):

    @inject
    def __init__(self, db: SQLAlchemy):
        super(RoleDao, self).__init__(Role, db)

