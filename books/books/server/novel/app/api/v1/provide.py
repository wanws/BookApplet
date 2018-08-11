"""
    Created by Amirk on 2018-07-30.
"""
from flask import Blueprint, g, current_app, request
from sqlalchemy import desc

from app.libs.error_code import Success, NotFound, AuthFailed, ErrorInsert
from app.libs.token_auth import auth
from app.model.base import db
from app.model.book_chapter import BookChapter
from app.model.book_novel_info import BookInfo
from app.model.user_book_case import UserBookCase
from app.plugin.novel_spider import Spider
from app.vaildators.forms import BookDetailForm, BookSectionForm, UserBookCaseForm
from app.view_model.spider_plugin import SpiderPluginFilter

api = Blueprint('provide', __name__)


@api.route('/v1/provide/get', methods=['GET'])
@auth.login_required
def get_user_book_index():
    """小程序首页api"""
    bookinfo = []
    spf = SpiderPluginFilter()
    books = UserBookCase.query.filter_by(openid=g.user.openid).all()
    for book in books:
        bookinfo.append(spf.check_bookinfo(temp={'_id': book.bookid}))
    data = {
        "recommend": current_app.config['RECOMMEND'],
        "books": bookinfo
    }
    return Success(data=data)


@api.route('/v1/provide/get_index', methods=['GET'])
def get_book_index():
    bookinfo = []
    spf = SpiderPluginFilter()
    books = current_app.config["BOOK_CASE_INIT"]
    for bookid in books:
        bookinfo.append(spf.check_bookinfo(temp={'_id': bookid}))
    data = {
        "recommend": current_app.config['RECOMMEND'],
        "books": bookinfo
    }
    return Success(data=data)


@api.route('/v1/provid/get_book_info', methods=['GET'])
def get_book_detail():
    """书籍信息页面"""
    form = BookDetailForm(request.args)
    if form.validate():
        id = form.data.get('bookid')
        spider = Spider(id)
        bookinfo = BookInfo.check_to_book(id=id)
        if bookinfo and bookinfo.get('longIntro') is not None:
            detail = bookinfo
        else:
            detail = spider.bookinfo_spider()
        rec = spider.book_recommend_spider()
        if len(rec) > 6:
            rec = rec[:6]
        data = {
            "detail": detail,
            "recommend": rec
        }
        return Success(data=data)
    return NotFound()


@api.route('/v1/provid/post_book', methods=['POST'])
@auth.login_required
def post_book():
    """保存/删除书架书籍"""
    form = UserBookCaseForm(data=request.json)
    if form.validate():
        bookid = form.data.get('bookid')
        type = form.data.get('type')  # 0 为删除 1 为添加
        books = UserBookCase.check_book_case(bookid, type)
        return Success(data=books)
    else:
        return ErrorInsert()


@api.route('/v1/provid/get_book_section', methods=['GET'])
# @auth.login_required
def get_book_section():
    """书籍目录"""
    form = BookSectionForm(data=request.args)
    if form.validate():
        id = form.data.get('bookid')
        page = form.data.get('page')
        books = BookChapter.slice_book_list(id[0], page[0])
        if books:
            data = books
        else:
            spider = Spider(id=id[0])
            try:
                data = spider.book_chapter_spider()
            except AttributeError:
                data = BookChapter.slice_book_list(id[0], page[0])
        return Success(data=data)
    return NotFound()
