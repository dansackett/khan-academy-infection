class BaseError(Exception):
    msg = "An error occured..."

    def __init__(self, msg=None):
        super(BaseError, self).__init__()
        if msg is not None:
            self.msg = msg

    def __str__(self):
        return self.msg

class WeightError(BaseError):
    msg = "Weights must be integer values"

class UserError(BaseError):
    msg = "User must be type user.User"

class ConnectionError(BaseError):
    msg = "Connections must be type user.User"

class FileError(BaseError):
    msg = "File format error. Please ensure each line has space separated connections and a weight."
