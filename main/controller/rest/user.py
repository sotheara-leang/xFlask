from injector import inject
from flask import request

from xflask.classy import route
from xflask.controller import Controller
from xflask.web.response import Response

from main.service.user import UserService
from main.controller.vo.user import UserVo
from main.model.user import User


class UserController(Controller):

    route_base = '/api/user'

    @inject
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    @route('')
    def get_all(self):
        users = self.user_service.get_all()
        return Response.success(users)

    @route('/<user_id>')
    def get(self, user_id):
        user = self.user_service.get(user_id)
        if user is None:
            return Response.not_found()

        return Response.success(user)

    @route('', methods=['POST'])
    def create(self):
        data = UserVo.deserialize_as_dict(request.get_json(), exclude=['id'])

        self.user_service.create(User(**data))

        return Response.success()

    @route('', methods=['PUT'])
    def update(self):
        data = UserVo.deserialize_as_dict(request.get_json())

        self.user_service.update(User(**data))

        return Response.success()

    @route('/<int:user_id>', methods=['DELETE'])
    def delete(self, user_id):
        if not self.user_service.exist(user_id):
            return Response.not_found()

        self.user_service.delete(user_id)

        return Response.success()
