"""
    Created by Amirk on 2018-07-26.
"""
import random
from urllib.parse import quote

import requests
from flask import current_app

from app.libs.error_code import NotFound
from app.view_model.spider_plugin import SpiderPluginFilter


class Spider:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"
    }
    error_str = "内容加载失败，请安装追书神器最新版继续阅读。更新版本后，如仍无法正常观看，请关注追书神器微信公众号，联系客服，获得帮助。"

    def __init__(self, id=None, query=None, author=None):
        self.host = current_app.config['BASE_API_HOST']
        self.id = id
        self.query = query
        self.author = author

    def request_get_url(self, url):
        res = requests.get(url, self.headers).json()
        return res

    def search_query(self):
        """搜索书籍"""
        url = self.host + f"/book/fuzzy-search?query={self.query}&start=0&limit=20"
        res = self.request_get_url(url)
        if len(res.get('books')) is not 0:
            spf = SpiderPluginFilter(res.get('books'))
            bookinfo = spf.parse_multiple()
        else:
            raise NotFound()
        return bookinfo

    def bookinfo_spider(self):
        """书籍详细信息"""
        url = self.host + f"/book/{self.id}"
        res = self.request_get_url(url)
        if res.get('_gg') is False:
            spf = SpiderPluginFilter()
            bookinfo = spf.check_bookinfo(res)
        else:
            raise NotFound()
        return bookinfo

    def book_recommend_spider(self):
        """推荐小说"""
        url = self.host + f"/book/{self.id}/recommend"
        res = self.request_get_url(url)
        if len(res.get('books')) is not 0:
            spf = SpiderPluginFilter(res.get('books'))
            bookinfo = spf.parse_multiple()
        else:
            raise NotFound()
        return bookinfo

    def book_author_spider(self):
        """精确搜索作者"""
        url = self.host + f"/book/accurate-search?author={self.author}&start=0&limit=4"
        res = self.request_get_url(url)
        if len(res.get('books')) is not 0:
            spf = SpiderPluginFilter(res.get('books'))
            bookinfo = spf.parse_multiple()
        else:
            raise NotFound()
        return bookinfo

    def book_chapter_spider(self):
        """书籍章节"""
        url = self.host + f"/mix-atoc/{self.id}?view=chapters"
        res = self.request_get_url(url)
        if res.get('ok') is True:
            spf = SpiderPluginFilter(res.get('mixToc'))
            chapterdata = spf.chapter_parse_save()
        else:
            raise NotFound()
        return chapterdata

    def book_chapter_text_spider(self, link):
        """书籍章节内容"""
        url = f"http://chapter2.zhuishushenqi.com/chapter/{link}"
        res = self.request_get_url(url)
        if res.get('chapter').get('body') not in self.error_str:
            spf = SpiderPluginFilter(res.get('chapter'))
            data = spf.chapter_text_save(link)
        else:
            raise NotFound()
        return data

    def book_search_sub_query(self, query):
        """搜索自动补充"""
        url = f"http://api.zhuishushenqi.com/book/auto-complete?query={query}"
        res = self.request_get_url(url)
        if res.get('ok') is True:
            return res.get('keywords')
        else:
            raise NotFound()

    def book_search_hot_words(self):
        """搜索热词"""
        url = f'http://api.zhuishushenqi.com/book/search-hotwords'
        res = self.request_get_url(url)
        hot_words = res.get('searchHotWords')
        hot_list = []
        count = 0
        for index, temp in enumerate(hot_words):
            if (index + 1) % 10 == 0:
                # print(hot_words[count:index + 1])
                hot_list.append(hot_words[count:index + 1])
                count += 10
        return hot_list[random.randint(0, 9)]

    def book_statistics_type(self):
        """获取所所有分类"""
        url = f"http://api.zhuishushenqi.com/cats/lv2/statistics"
        res = self.request_get_url(url)
        return res

    def book_by_categories_spider(self, data):
        """
            获取分类下得小说列表
            gender: 男生:mael 女生:female 出版:press
            type: 热门:hot 新书:new 好评:repulation 完结: over 包月: month
            major: 大类别 从接口1获取
            minor: 小类别 从接口4获取 (非必填)
            start: 分页开始页
            limit: 分页条数
        """
        url = f"https://api.zhuishushenqi.com/book/by-categories?gender={data.get('gender')}&type={data.get('type')}&major={data.get('name')}&minor=&start={data.get('start')}&limit=20"
        res = self.request_get_url(url)
        if res.get('ok') is True:
            books = res.get('books')
            data = []
            for book in books:
                book['cover'] = book.get('cover').replace('%2F', '/').replace('/agent/', '').replace('%3A', ':')
                data.append(book)
            return data
        else:
            raise NotFound()
