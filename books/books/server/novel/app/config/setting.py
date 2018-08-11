"""
    Created by Amirk on 2018-07-26.
"""

# 用户注册时, 默认书架

BOOK_CASE_INIT = ["50864bf69dacd30e3a000014", "50bee5da2033d09b2f000020",
                  "520da5d2dd2dfa6926000fc0", "50865988d7a545903b000009",
                  "523a89f3d87e739d3a005f30"]

# 推荐栏 , 暂只支持一个推荐
RECOMMEND = [
    {
        "bookid": "57aab46d50e9636041dbeca2",
        "title": "地府朋友圈",
        "rec_lang": "朋友圈内惊现牛头马面阎罗王"
    }
]

# token 过期时间
TOKEN_EXPIRATION = 30 * 24 * 3600