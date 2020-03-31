from xflask.type import Enum


class SysCode(Enum):

    SUCCESS                 = '00000', 'Success'
    SYS_ERROR               = '10001', 'Internal Server Error'
    INVALID                 = '10003', 'Request Invalid'
    NOT_FOUND               = '10004', 'Resource Not Found'
    EXISTED                 = '10005', 'Resource Existed'
    AUTH_INVALID            = '10006', 'Authentication Invalid'

    API_NOT_AVAILABLE       = '10007', 'API Not Available'
