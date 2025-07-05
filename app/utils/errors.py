class OTPError(Exception):
    """
    Base class for all OTP-related errors.
    """
    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(detail)


class OTPReadError(OTPError):
    """
    Raised when there is an issue reading or validating an OTP.
    """
    def __init__(self, detail: str, status_code: int):
        self.status_code = status_code
        super().__init__(detail)
