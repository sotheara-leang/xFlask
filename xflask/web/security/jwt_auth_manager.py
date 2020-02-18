from flask_jwt_extended import JWTManager, get_jwt_identity

from .auth_manager import AuthManager


class JwtAuthManager(AuthManager):

    def init(self, server):
        JWTManager(server.app)

    def get_current_user(self):
        return get_jwt_identity()
