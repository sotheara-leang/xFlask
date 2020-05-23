from injector import inject

from main.controller.vo.auth import LoginVo
from main.service.user import UserService
from xflask.web import route, JsonBody
from xflask.web.controller import Controller
from xflask.web.rest.response import Response


class AuthController(Controller):

    @inject
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    @route('/api/login', methods=['POST'])
    def login(self, login_vo: JsonBody(LoginVo)):
        token = self.user_service.auth(login_vo.username, login_vo.password)

        return Response.success({'token': token})
