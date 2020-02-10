from flask import Blueprint, request

from xflask.web.response import Response
from main.service.user import UserService
from main.model.user import User

bp = Blueprint('user', __name__, url_prefix='/api/user')

@bp.route('')
def get_users(user_service: UserService):
    users = user_service.get_users()

    results = []
    for user in users:
        results.append(user.to_dict())

    return Response.success(results).to_dict()

@app.route('<user_id>')
def get_user(user_id, user_service: UserService):
    user = user_service.get_user(user_id)
    return Response.success(user).to_dict()

@bp.route('', methods=['POST'])
def create_user(user_service: UserService):
    user = User(**request.get_json())
    user_service.create_user(user)
    return Response.success().to_dict()
