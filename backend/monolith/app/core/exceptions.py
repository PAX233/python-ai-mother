from app.core.error_codes import ErrorCode


class BusinessException(Exception):
    def __init__(self, code: ErrorCode, message: str) -> None:
        self.code = int(code)
        self.message = message
        super().__init__(message)

