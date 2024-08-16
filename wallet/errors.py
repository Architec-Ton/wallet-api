class APIException(Exception):
    def __init__(self, error: str, status_code: int = 400):
        self.error = error
        self.status_code = status_code
