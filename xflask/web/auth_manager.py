from flask_jwt_extended import JWTManager


class AuthManager(object):

    def init(self, server):
        pass


class JWTAuthManager(AuthManager):

    def init(self, server):
        JWTManager(server.app)


