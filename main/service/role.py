from injector import inject

from xflask.service import Service

from main.dao.role import RoleDao


class RoleService(Service):

    @inject
    def __init__(self, dao: RoleDao):
        super(RoleService, self).__init__(dao)

