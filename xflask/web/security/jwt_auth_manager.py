from flask_jwt_extended import JWTManager, get_jwt_identity, unset_jwt_cookies

from .auth_manager import AuthManager


class JwtAuthManager(AuthManager):

    def init(self, application):
        JWTManager(application.app)

    def get_current_user(self):
        return get_jwt_identity()

    def logout(self):
        unset_jwt_cookies()
