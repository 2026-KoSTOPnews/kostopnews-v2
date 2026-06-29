from app.exceptions.error_code import ErrorCode
from app.exceptions.status_code import StatusCode

class CustomException(Exception):
    def __init__(self, status: StatusCode, error: ErrorCode, detail: str | None = None):
        self.status = status
        self.error = error
        self.detail = detail