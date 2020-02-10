class StatusCode(object):

    def __init__(self, code, msg):
        self.code = code
        self.msg = msg


# status code

SC_SUCCESS          = StatusCode('0000', 'success')
SC_SYS_ERROR        = StatusCode('1001', 'internal server error')
SC_INVALID          = StatusCode('1003', 'request invalid')
SC_NOT_FOUND        = StatusCode('1004', 'resource not found')
SC_AUTH_INVALID     = StatusCode('1005', 'authentication invalid')
