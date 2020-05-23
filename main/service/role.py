from injector import inject

from xflask.service import CrudService

from main.dao.role import RoleDao


class RoleService(CrudService):

    @inject
    def __init__(self, dao: RoleDao):
        super(RoleService, self).__init__(dao)
