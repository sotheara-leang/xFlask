from flask_jwt_extended import JWTManager, get_jwt_identity


class AuthManager(object):

    def init(self, server):
        pass

    def get_current_user(self):
        pass

class SimpleJWTAuthManager(AuthManager):

    def init(self, server):
        JWTManager(server.app)

    def get_current_user(self):
        return get_jwt_identity()
