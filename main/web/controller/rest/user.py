from injector import inject

from main.model.user import User
from main.service.user import UserService
from main.web.form.user import UserForm, UserPageForm
from xflask.sqlalchemy.util import Page
from xflask.web import route
from xflask.web.controller import Controller
from xflask.web.response import Response


class UserController(Controller):
    route_base = '/api/user/'

    @inject
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    @route('')
    def get_all(self):
        users = self.user_service.get_all()
        return Response.success(users)

    @route('<int:user_id>')
    def get(self, user_id):
        user = self.user_service.get(user_id)
        if user is None:
            return Response.not_found()

        return Response.success(user)

    @route('page', methods=['POST'])
    def get_page(self, page_form: UserPageForm):
        pagination = self.user_service.get_page_by_filter(page_form.get_page(), page_form.get_per_page(),
                                                          page_form.get_sort(),
                                                          page_form.get_filter())
        page = Page.from_pagination(pagination)

        return Response.success(page)

    @route('', methods=['POST'])
    def create(self, user_form: UserForm(exclude=['id'])):
        self.user_service.create(User(**user_form.data))

        return Response.success()

    @route('', methods=['PUT'])
    def update(self, user_form: UserForm):
        self.user_service.update(User(**user_form.data))

        return Response.success()

    @route('<int:user_id>', methods=['DELETE'])
    def delete(self, user_id):
        if not self.user_service.exist(user_id):
            return Response.not_found()

        self.user_service.delete(user_id)

        return Response.success()
