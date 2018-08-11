"""
    Created by Amirk on 2018-07-26.
"""

BASE_API_HOST = "http://api.zhuishushenqi.com"

# APPID
APPID = "wx20d0b0a508db6871"

# SECRET
APP_SECRET_KEY = "58760318c34ed619eb2b214dd8aa54c7"

# 数据库链接字符串 dialect+driver://username:password@host:port/database
# 链接数据库类型
DIALECT = 'mysql'
# python操作数据库使用的驱动
DRIVER = 'cymysql'
# 用户名
USERNAME = 'root'
# 密码
PASSWORD = 'root'
# host是连接数据库的域名
HOST = '127.0.0.1'
# 端口号
PORT = '3306'
# 链接的数据库
DATABASE = 'novel_book'
# 链接字符串
SQLALCHEMY_DATABASE_URI = f"{DIALECT}+{DRIVER}://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}?charset=utf8"

SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_COMMIT_TEARDOWN = True

SECRET_KEY = '\x88D\xf09\xa0A\xc5V\xbe\x8b\xef\xd7\xd8\xd3\xe6\x98*4'
