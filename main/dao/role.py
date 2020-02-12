from xflask.dao import Dao

from main.model.role import Role


class RoleDao(Dao):

    def get_roles(self):
        return Role.query.all()

    def get_role(self, role_id):
        return Role.query.get(role_id)

    def create_role(self, role: Role):
        self.add(role)
        self.commit()
