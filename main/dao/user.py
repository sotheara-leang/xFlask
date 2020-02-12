from xflask.dao import Dao

from main.model.user import User


class UserDao(Dao):

    def get_users(self):
        return User.query.all()

    def get_user(self, user_id):
        return User.query.get(user_id)

    def get_user_by_username(self, username):
        return User.query.filter_by(username=username).first()

    def create_user(self, user: User):
        self.add(user)
        self.commit()
