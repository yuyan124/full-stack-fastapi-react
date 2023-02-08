from typing import AnyStr, Dict, Optional

from fastapi import HTTPException
from pydantic import PydanticValueError


class ApiException(HTTPException):
    status_code = 400
    code = 1000
    msg = "ok"

    def __init__(
        self,
        status_code=None,
        code=None,
        detail="错误",
        headers: dict = None,
    ) -> None:
        if status_code:
            self.status_code = status_code
        if code:
            self.code = code
        if detail:
            self.detail = detail
        if headers:
            self.headers = headers


class Success(ApiException):
    status_code = 200
    code = 1000
    msg = "ok"


class NotFound(ApiException):
    status_code = 400
    code = 1001
    msg = "该资源不存在."


class ParameterError(ApiException):
    status_code = 400
    code = 1002
    msg = "参数校验错误,请检查提交的参数信息"


class Unauthorized(ApiException):
    status_code = 401
    code = 1011
    msg = "未经授权的许可"


class Forbidden(ApiException):
    status_code = 403
    code = 1012
    msg = "失败！当前访问没有权限，或操作的数据没权限!"


class MethodNotAllowed(ApiException):
    status_code = 405
    code = 1013
    msg = "不允许使用此方法提交访问"


class UserExist(ApiException):
    status_code = 200
    code = 2001
    msg = "用户已存在！"


class UserNotExist(ApiException):
    status_code = 200
    code = 2002
    msg = "用户不存在！"


class NicknameExist(ApiException):
    status_code = 200
    code = 2003
    msg = "昵称已存在"


class ParameterValid(ApiException):
    status_code = 400
    code = 2004
    msg = "参数验证失败."


class InvalidToken(ApiException):
    status_code = 401
    code = 2005
    msg = "令牌失效"


class ExpiredToken(ApiException):
    status_code = 422
    code = 2006
    msg = "令牌过期"


class IncorrectEmailOrPassword(ApiException):
    status_code = 400
    code = 2007
    msg = "账号或密码错误。"


class InactiveUser(ApiException):
    status_code = 400
    code = 2008
    msg = "未激活的用户。"


class PermissionDenied(ApiException):
    status_code = 400
    code = 2009
    msg = "没有足够的权限。"


class AuthFailed(ApiException):
    status_code = 401
    error_code = 2007
    msg = "认证失败!"
    headers = {"WWW-Authenticate": "Bearer"}


class PasswordLengthError(PydanticValueError):
    code = "password.length"
    msg_template = "密码长度应大于等于6位"
