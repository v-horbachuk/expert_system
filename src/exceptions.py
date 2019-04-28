class NoContentError(Exception):
    def __init__(self, message="File is empty"):
        super().__init__(message)


class BadConditionError(Exception):
    def __init__(self, string):
        message = f"Condition error: {string}"
        super().__init__(message)


class BadStringError(Exception):
    def __init__(self, string):
        message = f"Line is not valid {string}"
        super().__init__(message)
