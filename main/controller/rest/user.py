from flask import Blueprint, request

from xflask.web.response import Response
from main.service.user import UserService
from main.model.user import User


bp = Blueprint('user', __name__, url_prefix='/api/user')


@bp.route('')
def get_users(user_service: UserService):
    users = user_service.get_all()
    users = [e.to_dict() for e in users]
    return Response.success(users).to_dict()


@bp.route('/<user_id>')
def get_user(user_id, user_service: UserService):
    user = user_service.get_by_id(user_id)
    if user is None:
        return Response.not_found().to_dict()

    return Response.success(user.to_dict()).to_dict()


@bp.route('', methods=['POST'])
def create_user(user_service: UserService):
    user = User(**request.get_json())
    user_service.create_user(user)
    return Response.success().to_dict()


@bp.route('', methods=['PUT'])
def update_user(user_service: UserService):
    json = request.get_json()

    return Response.success().to_dict()


@bp.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id, user_service: UserService):
    user = user_service.get_by_id(user_id)
    if user is None:
        return Response.not_found().to_dict()

    user_service.delete(user)

    return Response.success().to_dict()
