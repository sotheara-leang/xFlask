from xflask.type import Enum


class SysCode(Enum):

    SUCCESS                 = '00000', 'Success'
    SYS_ERROR               = '00001', 'Internal Server Error'
    INVALID                 = '00002', 'Request Invalid'
    NOT_FOUND               = '00003', 'Resource Not Found'
    EXISTED                 = '00004', 'Resource Existed'
    AUTH_INVALID            = '00005', 'Authentication Invalid'
    API_NOT_AVAILABLE       = '00006', 'API Not Available'
