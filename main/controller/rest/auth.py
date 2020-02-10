from flask import request

from xflask.web.response import Response

from main import app
from main.service.user import UserService
from main.controller.vo.auth import LoginVo


@app.route('/api/login', methods=['POST'])
def login(user_service: UserService):
    login_vo = LoginVo.load(request.get_json())

    token = user_service.auth(login_vo.username, login_vo.password)

    return Response.success({'token': token}).to_dict()

