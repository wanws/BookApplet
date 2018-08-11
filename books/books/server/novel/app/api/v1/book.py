"""
    Created by Amirk on 2018-07-26.
"""
from flask import Blueprint, request
from app.libs.error_code import Success, NotFound
from app.libs.token_auth import auth
from app.model.book_chapter import BookChapter
from app.model.book_novel_info import BookInfo
from app.plugin.novel_spider import Spider
from app.vaildators.forms import ContentTextForm, BookByCategorieForm

api = Blueprint('book', __name__)


@api.route('/v1/book/search')
def search():
    """搜索书籍"""
    form = ContentTextForm(request.args)
    if form.validate():
        query = form.data.get('query')
        bookinfo = BookInfo.check_to_book(title=query)
        if bookinfo:
            data = bookinfo
        else:
            spider = Spider(query=query)
            data = spider.search_query()
            print(data)
        return Success(data=data)
    return NotFound()


@api.route('/v1/book/bookinfo/<string:id>')
def bookinfo(id):
    """书籍详情信息"""
    bookinfo = BookInfo.check_to_book(id=id)
    if bookinfo and bookinfo.get('longIntro') is not None:
        datas = bookinfo
    else:
        spider = Spider(id)
        datas = spider.bookinfo_spider()
    return Success(data=datas)


@api.route('/v1/book/<string:id>/recommend')
def book_recommend(id):
    """推荐小说"""
    spider = Spider(id=id)
    data = spider.book_recommend_spider()
    return Success(data=data)


@api.route('/v1/book/accurate')
def accurate_author():
    """精确作者搜索"""
    author = request.args.get('author')
    book_author = BookInfo.check_to_book(author=author)
    if book_author:
        data = book_author
    else:
        spider = Spider(author=author)
        data = spider.book_author_spider()
    return Success(data=data)


@api.route('/v1/book/chapter/<string:id>')
def book_chapter_list(id):
    """书籍目录"""
    books = BookChapter.check_to_book_chapter(id)
    if books:
        data = books
    else:
        spider = Spider(id=id)
        data = spider.book_chapter_spider()
    return Success(data=data)


@api.route('/v1/book/chapter/parse')
@auth.login_required
def book_chpater_text():
    """章节内容"""
    form = ContentTextForm(request.args)
    if form.validate():
        query = form.data.get('query')
        books = BookChapter.check_to_book_text(query)
        if books:
            content_text = books
        else:
            spider = Spider()
            content_text = spider.book_chapter_text_spider(query)
        content_text['chapterText'] = [temp for temp in content_text.get('chapterText').split('\n')]
        content__on_down = BookChapter.check_to_text_on_or_down(query)  # 返回的下一章
        data = {
            "content_text": content_text,
            "content__on_down": content__on_down
        }
        return Success(data=data)
    return NotFound()


@api.route('/v1/book/search_sub')
def search_sup_query():
    """搜索自动补充"""
    form = ContentTextForm(request.args)
    if form.validate():
        query = form.data.get('query')
        spider = Spider()
        data = spider.book_search_sub_query(query)
    return Success(data=data)


@api.route('/v1/book/hot_words')
def hot_words():
    """搜索热词"""
    spider = Spider()
    data = spider.book_search_hot_words()
    return Success(data=data)


@api.route('/v1/book/statistics')
def book_statistics():
    """获取所有分类"""
    spider = Spider()
    data = spider.book_statistics_type()
    return Success(data=data)

@api.route('/v1/book/by-categories')
def book_by_categories():
    """
    根据分类获取小说列表
    """
    spider = Spider()
    form = BookByCategorieForm(request.args)
    if form.validate():
        data = spider.book_by_categories_spider(form.data)
        return Success(data=data)
    else:
        return NotFound()