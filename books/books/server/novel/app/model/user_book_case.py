"""
    Created by Amirk on 2018-07-30.
"""
from flask import current_app, g

from app.model.base import Base, db
from sqlalchemy import Column, Integer, String

"""
openid  # 用户id
bookid  # 书籍id
"""


class UserBookCase(Base):
    id = Column(Integer, primary_key=True)
    openid = Column(String(100), nullable=False)
    bookid = Column(String(100), nullable=False)

    def keys(self):
        return ('openid', 'bookid')

    @staticmethod
    def user_init_book(openid):
        """当用户注册的时, 默认给用户书架添加5本书籍"""

        books = current_app.config['BOOK_CASE_INIT']
        try:
            for bookid in books:
                with db.auto_commit():
                    user = UserBookCase()
                    user.openid = openid
                    user.bookid = bookid
                    db.session.add(user)
        except:
            return False
        return True

    @staticmethod
    def check_book_case(bookid, type):
        """删除/添加书籍"""
        book = UserBookCase.query.filter_by(bookid=bookid).first()
        if book:
            if type is 0:
                with db.auto_commit():
                    book.status = 0
                    db.session.add(book)
        else:
            if type is 1:
                with db.auto_commit():
                    book = UserBookCase()
                    book.bookid = bookid
                    book.openid = g.user.openid
                    db.session.add(book)
        books = UserBookCase.query.filter_by(openid=g.user.openid).all()
        return [dict(book) for book in books]
