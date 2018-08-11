"""
    Created by Amirk on 2018-07-29.
"""
import json

from flask import Blueprint, request

from app.libs.error_code import Success, ErrorInsert
from app.libs.token_auth import get_token
from app.plugin.requests_wx import RquestWxSessionKey
from app.vaildators.forms import UserInfoForm

api = Blueprint('user', __name__)


@api.route('/v1/user/login', methods=['POST'])
def getuserinfo():
    # 保存用户信息
    form = UserInfoForm(data=request.json)
    if form.validate():
        request_wx = RquestWxSessionKey(form.data)
        userinfo = request_wx.getparse()
        userinfo["token"] = get_token(userinfo)
        return Success(data=userinfo)
    else:
        return ErrorInsert()
