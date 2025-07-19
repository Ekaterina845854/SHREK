from fastapi import HTTPException, status


class NotFoundError(HTTPException):
    def __init__(self, detail = None, headers = None):
        super().__init__(status.HTTP_404_NOT_FOUND, detail, headers)
        

class NoPermissionsError(HTTPException):
    def __init__(self, detail = None, headers = None):
        super().__init__(status.HTTP_403_FORBIDDEN, detail, headers)