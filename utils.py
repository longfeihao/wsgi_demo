class CommonException(Exception):
    code = "0"
    message = "system busy"

    def __init__(self, code, message="system busy"):
        super(CommonException, self).__init__()
        if code:
            self.code = code
        if message:
            self.message = message

