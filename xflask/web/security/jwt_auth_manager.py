from flask_jwt_extended import JWTManager, get_jwt_identity, get_raw_jwt

from xflask.web.security.auth_manager import AuthManager


class JwtAuthManager(AuthManager):

    blacklist = set()

    def init(self, application):
        self.jwt_manager = JWTManager(application.app)

        @self.jwt_manager.token_in_blacklist_loader
        def check_if_token_in_blacklist(decrypted_token):
            jti = decrypted_token['jti']
            return jti in self.blacklist

    def get_current_user(self):
        return get_jwt_identity()

    def logout(self):
        jti = get_raw_jwt()['jti']
        self.blacklist.add(jti)
