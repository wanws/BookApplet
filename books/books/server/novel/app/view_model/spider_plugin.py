"""
    Created by Amirk on 2018-07-26.
"""
# 返回搜索小说数据
from urllib.parse import quote
from app.model.base import db
from app.model.book_chapter import BookChapter
from app.model.book_novel_info import BookInfo

"""
书籍信息

id  # 书籍 id 号
author # 书籍作者
cat    # 分类
contentType  # 小说内容类型
cover   # 小说封面
title   # 书名
wordCount # 书籍字数
score         # 书籍评分
latelyFollower  # 追看人数
retentionRatio  # 读者存留率

updated      # 最近更新时间
lastChapter  # 最新章节
chaptersCount  # 章节数
longIntro   # 简介
"""

"""
书籍章节

id # 书籍id
chaptersCount # 书籍章节数
chaptersUpdated # 最新更新时间
chapterTile  # 章节名 
chapterLink  # 链接
"""


class SpiderPluginFilter:
    """
    1. 获取书籍信息
    2. 保存书籍数据至数据库
    """

    def __init__(self, res=None):
        self.res = res

    def parse_multiple(self):
        bookinfo = [self.check_bookinfo(temp) for temp in self.res]
        return bookinfo

    def check_bookinfo(self, temp):
        """
        检测数据库中是否有当前书籍信息
        如果有则返回书籍信息, 否则先保存数据库
        再返回书籍信息
        """
        bookinfo = BookInfo.query.get(temp.get('_id'))
        if bookinfo is None:
            with db.auto_commit():
                bookinfo = BookInfo()
                bookinfo.id = temp.get('_id'),
                bookinfo.author = temp.get('author'),
                bookinfo.cat = temp.get('cat'),
                bookinfo.contentType = temp.get('contentType'),
                cover = temp.get('cover').replace('%2F', '/').replace('/agent/', '').replace('%3A', ':')
                bookinfo.cover = cover,
                bookinfo.title = temp.get('title'),
                bookinfo.wordCount = temp.get('wordCount'),
                bookinfo.latelyFollower = temp.get('latelyFollower'),
                bookinfo.retentionRatio = temp.get('retentionRatio'),
                self.check_bookinfo_parse(bookinfo, temp)
                db.session.add(bookinfo)
        elif bookinfo.longIntro is None:
            self.check_bookinfo_parse(bookinfo, temp)
            db.session.add(bookinfo)
        return dict(bookinfo)

    def check_bookinfo_parse(self, bookinfo, temp):
        with db.auto_commit():
            bookinfo.longIntro = temp.get('longIntro'),
            rating = temp.get('rating')
            if rating:
                bookinfo.score = rating.get('score')
            bookinfo.chaptersCount = temp.get('chaptersCount'),
            bookinfo.lastChapter = temp.get('lastChapter').replace(' ', ''),
            updated = temp.get('updated')
            if updated is not None:
                updated = updated.split('T')[0] + "  " + updated.split('T')[1].split('.')[0]
            bookinfo.updated = updated

    def chapter_parse_save(self):
        """保存章节"""
        books = BookChapter.query.filter_by(bookinfo_id=self.res.get('book')).all()
        if len(books) != len(self.res.get('chapters')):
            for temp in self.res.get('chapters'):
                with db.auto_commit():
                    books = BookChapter()
                    books.bookinfo_id = self.res.get('book')
                    books.chaptersCount = self.res.get('chaptersCount')
                    books.chaptersUpdated = self.res.get('chaptersUpdated')
                    books.chapterTile = temp.get('title')
                    books.chapterLink = quote(temp.get('link'))
                    db.session.add(books)
        return [dict(book) for book in books]

    def chapter_text_save(self, link):
        """保存章节内容"""
        books = BookChapter.query.filter_by(chapterLink=link).first()
        if books.chapterText is None or books.chapterText == "":
            with db.auto_commit():
                books.chapterText = self.res.get('body')
                books.chaptersCount = len(self.res.get('body'))
                db.session.add(books)
        return dict(books)
