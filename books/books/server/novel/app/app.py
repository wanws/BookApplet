"""
    Created by Amirk on 2018-07-26.
"""
from flask import Flask


def blueprint_register(app):
    """注册蓝图"""
    from app.api.v1 import book, user, provide
    app.register_blueprint(book.api)
    app.register_blueprint(user.api)
    app.register_blueprint(provide.api)


def register_plugin(app):
    """注册插件"""
    from app.model.base import db
    db.init_app(app)
    with app.app_context():
        db.create_all()


def created_app():
    """创建Flask  核心 app"""
    app = Flask(__name__)

    app.config.from_object('app.config.secure')
    app.config.from_object('app.config.setting')

    blueprint_register(app)
    register_plugin(app)

    return app
