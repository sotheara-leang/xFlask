from injector import inject

from main.service.user import UserService
from main.web.form.auth import LoginForm
from xflask.web import route
from xflask.web.controller import Controller
from xflask.web.response import Response

from xflask.web.security import logout


class AuthController(Controller):

    @inject
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    @route('/api/login', methods=['POST'])
    def login(self, login_form: LoginForm):
        token = self.user_service.auth_user(login_form.username.data, login_form.password.data)

        return Response.success({'token': token})

    @route('/api/logout', methods=['POST'])
    def logout(self):
        logout()

        return Response.success()

