from xflask.common import *

def get_current_user():
    auth_manager = get_xflask().auth_manager
    return auth_manager.get_current_user()

def logout():
    auth_manager = get_xflask().auth_manager
    return auth_manager.logout()
