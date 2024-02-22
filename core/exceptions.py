
class Error(Exception):
    default = {
        "message": None,
        "code": None
    }

    def __init__(self, message=None, code=None, **kwargs):
        self.message = message or self.default["message"]
        self.code = code or self.default["code"]
        self.context = kwargs
        super(Error, self).__init__(message)

    def __str__(self):
        return self.message


class UserNotFoundError(Error):
    message = "User Not found in DB"


class UserAlreadyExists(Error):
    default = {
        "message": "User Already Exists in the DB",
        "code": "EXISTS"
    }


