from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

def bad_request(detail="Bad request"):
    return HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=detail)

def not_found(detail="Not found"):
    return HTTPException(status_code=HTTP_404_NOT_FOUND, detail=detail)

def forbidden(detail="Forbidden"):
    return HTTPException(status_code=HTTP_403_FORBIDDEN, detail=detail)
