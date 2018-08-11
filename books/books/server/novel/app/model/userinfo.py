"""
    Created by Amirk on 2018-07-29.
"""
from app.model.base import Base
from sqlalchemy import Column, String, Integer, SmallInteger

"""
openid    # 用户id
nickName  # 用户名
gender    # 性别
avatarUrl # 头像
language  # 语言
city      # 城市
province  # 省,市
country   # 国家
"""


class UserInfo(Base):
    openid = Column(String(100), primary_key=True)
    nickName = Column(String(50))
    gender = Column(SmallInteger)
    avatarUrl = Column(String(200))
    language = Column(String(50))
    city = Column(String(50))
    province = Column(String(50))
    country = Column(String(50))

    def keys(self):
        return ('openid', 'nickName', 'gender',
                'avatarUrl', 'language', 'city',
                'province', 'country')
