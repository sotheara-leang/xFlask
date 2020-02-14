from xflask.type import Type


class StatusCode(Type):

    SUCCESS          = '00000', 'Success'
    SYS_ERROR        = '10001', 'Internal Server Error'
    INVALID          = '10003', 'Request Invalid'
    NOT_FOUND        = '10004', 'Resource not found'
    AUTH_INVALID     = '10005', 'Authentication Invalid'
