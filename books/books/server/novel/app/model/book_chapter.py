"""
    Created by Amirk on 2018-07-27.
"""
from urllib.parse import quote

from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship, backref

from app.libs.error_code import NotFound
from app.model.base import Base

"""
id # 书籍id
chaptersCount # 书籍章节数
chaptersUpdated # 最新更新时间
chapterTitle  # 章节名 
chapterLink  # 链接
"""


class BookChapter(Base):
    """书籍章节"""
    __tablename__ = "bookchapter"
    id = Column(Integer, primary_key=True)
    chaptersCount = Column(Integer)
    chaptersUpdated = Column(String(50))
    chapterTile = Column(String(100))
    chapterLink = Column(String(200), unique=True)
    chapterText = Column(Text)
    bookinfo_id = Column(String(100), ForeignKey('bookinfo.id'))
    bookinfo = relationship('BookInfo', backref=backref('bookchapter'))

    def keys(self):
        return ("id", "chapterTile", "chapterLink", "chapterText",
                "chaptersCount", "chaptersUpdated", "bookinfo_id")

    @staticmethod
    def check_to_book_chapter(id=None):
        """检测数据库书籍目录"""
        books = BookChapter.query.filter_by(bookinfo_id=id).all()
        if len(books) != 0:
            return [dict(book) for book in books]

    @staticmethod
    def slice_book_list(id, page):
        """书籍目录分页"""
        books = BookChapter.query.filter_by(bookinfo_id=id).slice((int(page) - 1) * 100, int(page) * 100).all()
        if len(books) != 0:
            return [dict(book) for book in books]
        return False

    @staticmethod
    def check_to_book_text(link):
        """检测章节内容"""
        books = BookChapter.query.filter_by(chapterLink=link).first()
        if books is not None:
            text = books.chapterText
            if text is not None and text != "":
                return dict(books)
        return False

    @staticmethod
    def check_to_text_on_or_down(link):
        """检测当前章节的上/下章link"""
        books = dict(BookChapter.query.filter_by(chapterLink=link).first())
        if books:
            count = 1
            id = books.get('id')
            bookid = books.get('bookinfo_id')
            try:
                while True:
                    down_id = id + count
                    down_book = dict(BookChapter.query.get(down_id))
                    if down_book.get('bookinfo_id') == bookid:
                        down_book = down_book
                        break
                    else:
                        down_book = []
                    count += 1
            except Exception:
                down_book = []

            try:
                while True:
                    on_id = id - count
                    if count > 5:
                        break
                    on_book = dict(BookChapter.query.get(on_id))
                    if on_book and on_book.get('bookinfo_id') == bookid:
                        on_book = on_book
                        break
                    else:
                        on_book = []
                    count += 1
            except Exception:
                on_book = []

            book_on_down_data = {
                "on_book": on_book,
                "down_book": down_book
            }
            return book_on_down_data
        return False
