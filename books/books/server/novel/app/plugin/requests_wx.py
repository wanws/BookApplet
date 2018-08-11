"""
    Created by Amirk on 2018-07-29.
"""
import json

from flask import current_app
import requests
from app.model.base import db
from app.model.user_book_case import UserBookCase
from app.model.userinfo import UserInfo


class RquestWxSessionKey:
    """请求微信api 获取openid 保存用户信息到数据库"""

    def __init__(self, data):
        self.data = data
        self.session_key = None
        self.appId = current_app.config['APPID']
        self.secret = current_app.config['APP_SECRET_KEY']
        self.openId = None
        self.userinfo = self.data.get('userinfo')
        self.url = f"https://api.weixin.qq.com/sns/jscode2session?" \
                   f"appid={self.appId}" \
                   f"&secret={self.secret}" \
                   f"&js_code={self.data.get('code')}" \
                   f"&grant_type=authorization_code"

    def getparse(self):
        res = requests.get(self.url).json()
        self.session_key = res.get('session_key')
        self.openId = res.get('openid')
        self.userinfo["openid"] = self.openId
        return self.save_user_info()

    def save_user_info(self):
        user = UserInfo.query.get(self.userinfo.get('openid'))
        if not user:
            with db.auto_commit():
                user = UserInfo()
                user.openid = self.userinfo.get('openid')
                user.nickName = self.userinfo.get('nickName')
                user.avatarUrl = self.userinfo.get('avatarUrl')
                user.gender = self.userinfo.get('gender')
                user.language = self.userinfo.get('language')
                user.city = self.userinfo.get('city')
                user.province = self.userinfo.get('country')
                user.country = self.userinfo.get('country')
                db.session.add(user)
                UserBookCase.user_init_book(self.openId)
        return dict(user)
