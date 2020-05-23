from injector import inject

from main.controller.vo.user import UserVo
from main.model.user import User
from main.service.user import UserService
from xflask.web import route, JsonBody
from xflask.web.controller import Controller
from xflask.web.rest.response import Response


class UserController(Controller):
    route_base = '/api/user/'

    @inject
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    @route('')
    def get_all(self):
        users = self.user_service.get_all()
        return Response.success(users)

    @route('<user_id>')
    def get(self, user_id):
        user = self.user_service.get(user_id)
        if user is None:
            return Response.not_found()

        return Response.success(user)

    @route('', methods=['POST'])
    def create(self, user: JsonBody(UserVo, exclude=['id'])):
        self.user_service.create(User(**user.__dict__))

        return Response.success()

    @route('', methods=['PUT'])
    def update(self, user: JsonBody(UserVo)):
        self.user_service.update(User(**user))

        return Response.success()

    @route('<int:user_id>', methods=['DELETE'])
    def delete(self, user_id):
        if not self.user_service.exist(user_id):
            return Response.not_found()

        self.user_service.delete(user_id)

        return Response.success()
