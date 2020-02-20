from flask import request

from xflask.web.response import Response
from xflask.classy import route
from xflask.controller import Controller

from main.service.user import UserService
from main.controller.vo.auth import LoginVo


class AuthController(Controller):

    @route('/api/login', methods=['POST'])
    def login(self, user_service: UserService):
        login_vo = LoginVo.deserialize(request.get_json())

        token = user_service.auth(login_vo.username, login_vo.password)

        return Response.success({'token': token})

