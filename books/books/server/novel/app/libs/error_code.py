"""
    Created by Amirk on 2018-07-27.
"""

from app.libs.error import APIExcption


class Success(APIExcption):
    code = 201
    error_code = 0
    msg = 'ok'


class NotFound(APIExcption):
    code = 404
    error_code = 1001
    msg = "The resource is not found "


class ErrorInsert(APIExcption):
    code = 403
    error_code = 1002
    msg = "Sorry, data error"


class AuthFailed(APIExcption):
    code  = 401
    error_code = 1005
    msg = 'authorization failed'