from flask import Blueprint, request

from xflask.web.response import Response
from main.service.user import UserService
from main.controller.vo.user import *


bp = Blueprint('user', __name__, url_prefix='/api/user')


@bp.route('')
def get_all(user_service: UserService):
    users = user_service.get_all()
    users = [e.to_dict() for e in users]
    return Response.success(users).to_dict()


@bp.route('/<user_id>')
def get(user_id, user_service: UserService):
    user = user_service.get(user_id)
    if user is None:
        return Response.not_found().to_dict()

    return Response.success(user.to_dict()).to_dict()


@bp.route('', methods=['POST'])
def create(user_service: UserService):
    data = CreateUserVo.load(request.get_json())
    user_service.create(data)

    return Response.success().to_dict()


@bp.route('', methods=['PUT'])
def update(user_service: UserService):
    data = request.get_json()

    return Response.success().to_dict()

@bp.route('/<user_id>', methods=['DELETE'])
def delete(user_id, user_service: UserService):
    user = user_service.get_by_id(user_id)
    if user is None:
        return Response.not_found().to_dict()

    user_service.delete(user)

    return Response.success().to_dict()
