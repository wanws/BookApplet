"""
    Created by Amirk on 2018-07-30.
"""
from collections import namedtuple

from flask import current_app, g
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from app.libs.error_code import AuthFailed

User = namedtuple('User', ['openid','type'])

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(token, secret):
    """验证用户"""
    user = verify_auth_token(token)
    if not user:
        return False
    else:
        g.user = user
        return True




def verify_auth_token(token):
    """token验证"""
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except BadSignature:
        raise AuthFailed(error_code=1002, msg='token is invalid')
    except SignatureExpired:
        raise AuthFailed(error_code=1003, msg='token is expired ')
    return User(
        openid=data.get('openid'),
        type=data.get('type')
    )



def get_token(userinfo):
    token = generate_auth_token(userinfo)
    return token.decode('ascii')


def generate_auth_token(userinfo, expiration=7200):
    s = Serializer(current_app.config['SECRET_KEY'],
                   expires_in=current_app.config['TOKEN_EXPIRATION'])

    return s.dumps({
        'openid': userinfo.get('openid'),
        'type': True
    })
