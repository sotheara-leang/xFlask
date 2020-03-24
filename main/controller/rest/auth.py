from injector import inject

from xflask.web.response import Response
from xflask.classy import route, JsonBody
from xflask.controller import Controller

from main.service.user import UserService
from main.controller.vo.auth import LoginVo


class AuthController(Controller):

    @inject
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    @route('/api/login', methods=['POST'])
    def login(self, login_vo: JsonBody(LoginVo)):
        token = self.user_service.auth(login_vo.username, login_vo.password)

        return Response.success({'token': token})

