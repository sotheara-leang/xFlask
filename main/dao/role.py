from xflask.dao import Dao

from main.model.role import Role


class RoleDao(Dao):

    def __init__(self):
        super(RoleDao, self).__init__(Role)

