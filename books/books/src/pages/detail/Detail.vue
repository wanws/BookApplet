<template>
    <div class="container">
      <div class="bookinfo">
        <img mode="aspectFit" :src="detail.cover">
        <div class="right_book">
          <div class="title">
            {{detail.title}}
          </div>
          <div class='rate'>
            <span>☆☆☆☆☆</span>
            <div class="hollow" :style="style">
              ★★★★★
            </div>
            <span class="span-text">{{detail.score}}分</span>
          </div>
          <div class="text_i">
            作者: {{detail.author}}
          </div>
          <div class="text_i">
            类型: 玄幻
          </div>
          <div class="text_i" v-if="detail.wordCount">
            字数: {{detail.wordCount}} 字
          </div>
        </div>
        <div class="updatedchapter" @click="check_directory(detail.id, detail.title)">
          <p >查看目录<span></span></p><span>最新:{{detail.lastChapter}}<img mode="aspectFit" src="../../../static/image/jiantou.png"></span>
        </div>
        <div class="jianjie">
          <p class="name">简介<span></span></p>
          <div class="jianjie_text">
            <p>
              {{detail.longIntro}}
            </p>
            <!--<img @click="click_jianjie_img" mode="aspectFit" src="../../../static/image/xiajiantou.png">-->
          </div>
        </div>
      </div>
      <div class="recommend">
        <p class="name">推荐小说<span></span></p><span class="refresh" @click="click_refresh">换一换</span>
        <ul class="books">
          <li  class="book-list":key="r.index" v-for="r in rec" @click="click_rec(r.id)">
            <img mode="aspectFit" :src="r.cover" alt="">
            <div class="title">
              {{r.title}}
            </div>
            <div class="book-chapter">
              <span v-if="r.updated">更新时间:2018-3-2</span>
              <p>{{r.lastChapter}}</p>
              <div class="list-border">
              </div>
            </div>
          </li>
          <div class="hetight_div">

          </div>
        </ul>
      </div>
      <div class="operation">
          <div class="addbook" @click="add_click">
            <div v-if="opertion.active === true"><img mode="aspectFit" src="../../../static/image/jiahao.png"><p :style="add_style">{{opertion.str}}</p></div>
            <div v-else><img mode="aspectFit" src="../../../static/image/jianhao.png"><p>{{opertion.str}}</p></div>
          </div>
        <div class="readbook" @click="read_click">
          开始阅读
        </div>
      </div>
    </div>
</template>

<script>
  import config from '@/config'
  import {get, showModalLogin, post, showSuccess, showLoadings} from '../../utils'
  const Base64 = require('js-base64').Base64
  export default {
    data () {
      return {
        bookid: '', // 当前书籍id
        detail: [], // 当前书籍信息
        rec: [], // 推荐 保存3个内容
        temp: [], //  推荐 保存3个内容  临时 存储 和 rec 互换 内容
        userinfo: [], // 用户信息你
        books: [], // 书架列表
        book: {}, // 书籍阅读缓存
        bookchapter: [], // 当前 0-100章内容
        opertion: { // 移除/添加书架 控制
          str: '添加书架',
          active: true
        }
      }
    },
    mounted () {
      this.detail = []
      // 修改标题
      this.bookdetail()
      this.bookid = this.$root.$mp.query.bookid
      // 获取缓存中得用户信息
      this.getUserStopage()
      // 获取缓存中得书架列表
      this.getSopageBooks()
      // 请求server
      this.getServerDetail()
      // 判断当前书籍id是否在书架中
      this.is_bookid_in_books()
      // 验证当前书籍是否阅读过
      this.is_in_Storage_bookid()
      // 请求server 获取前100章
      this.getServerSection()
    },
    computed: {
      style () {
        return `width:${this.detail.score / 2.3}em`
      },
      add_style () {
        return 'color: #EA5149'
      }
    },
    onLoad () {
      // 加载中
      showLoadings()
    },
    onShow () {
    },
    methods: {
      // 验证缓存中是否有当前书籍阅读历史
      is_in_Storage_bookid () {
        this.book = wx.getStorageSync(this.bookid)
        if (!this.book) {
          this.book = {}
        }
      },
      // 验证用户是否登录
      is_userinfo () {
        if (this.userinfo === '') {
          console.log('userinfo null')
          showModalLogin()
        } else {
          return true
        }
      },
      // 点击看书
      read_click () {
        console.log('click read')
        if (this.is_userinfo()) {
          if (this.book.bookid) {
            wx.navigateTo({
              url: '/pages/content/main?title=' + this.detail.title + '&link=' + this.book.content.chapterLink
            })
          } else {
            wx.navigateTo({
              url: '/pages/content/main?title=' + this.detail.title + '&link=' + this.bookchapter[0].chapterLink
            })
          }
        }
      },
      // 请求目录  server 获取前100章
      async getServerSection () {
        const header = {
          'content-type': 'application/json',
          'Authorization': 'Basic' + ' ' + Base64.encode(this.userinfo.token + ':password')
        }
        const data = {
          bookid: this.bookid,
          page: 1
        }
        const chapter = await get(config.sectionUrl, data, header)
        this.bookchapter = chapter
      },
      // 获取server 端数据
      async getServerDetail () {
        const header = {
          'content-type': 'application/json',
          'Authorization': 'Basic' + ' ' + Base64.encode(this.userinfo.token + ':password')
        }
        const data = {
          bookid: this.bookid
        }
        const books = await get(config.detailUrl, data, header)
        this.detail = books.detail
        // this.rec = books.recommend
        for (let i = 0; i < (books.recommend.length - 1) / 2; i++) {
          this.rec[i] = books.recommend[i]
          this.temp[i] = books.recommend[(books.recommend.length - 1) - i]
        }
        // 书籍评分 保留两位小数
        this.detail.score = Number(books.detail.score).toFixed(2)
      },
      // 判断当前书籍id是否在书架中
      is_bookid_in_books () {
        for (let i = 0; i < this.books.length; i++) {
          if (this.bookid === this.books[i].id && this.userinfo !== '') {
            this.opertion.str = '移除书架'
            this.opertion.active = false
            break
          } else {
            this.opertion.str = '添加书架'
            this.opertion.active = true
          }
        }
      },
      // 添加/删除书籍
      async postServerAdd (type) {
        const header = {
          'content-type': 'application/json',
          'Authorization': 'Basic' + ' ' + Base64.encode(this.userinfo.token + ':password')
        }
        let data = {
          bookid: this.bookid,
          type: type // 0 为移除  1 为添加
        }
        const res = await post(config.postBookUrl, data, header)
        // 书架列表更新
        wx.setStorageSync('books', res)
      },
      // 点击添加书架
      add_click () {
        console.log('click add')
        if (this.is_userinfo()) {
          if (!this.opertion.active) {
            // 移除书架
            this.postServerAdd(0)
            this.opertion.str = '添加书架'
            this.opertion.active = true
            // 将当前书籍缓存删除
            wx.removeStorageSync(this.bookid)
            showSuccess('移除成功')
          } else {
            this.postServerAdd(1)
            this.opertion.str = '移除书架'
            this.opertion.active = false
            showSuccess('添加成功')
          }
        } else {

        }
      },
      // 获取缓存中得书架列表
      getSopageBooks () {
        this.books = wx.getStorageSync('books')
      },
      // 获取用户信息缓存
      getUserStopage () {
        this.userinfo = wx.getStorageSync('userinfo')
      },
      // 查看目录
      check_directory (bookid, title) {
        console.log('查看目录' + bookid)
        wx.navigateTo({
          url: '/pages/section/main?bookid=' + bookid + '&title=' + title
        })
      },
      // 点击换一换
      click_refresh () {
        console.log('clcik 换一换')
        let refresh = this.rec
        this.rec = this.temp
        this.temp = refresh
      },
      // 推荐列表点击
      click_rec (bookid) {
        console.log('clcik ' + bookid)
        wx.navigateTo({
          url: '/pages/detail/main?bookid=' + bookid
        })
      },
      // 点击简介更多
      click_jianjie_img () {
        console.log('clcik 下箭头')
      },
      // 修改标题
      bookdetail () {
        wx.setNavigationBarTitle({
          title: '书籍详情'
        })
      }
    }
  }
</script>
<style lang="scss">
  body{
    background: #f0f1f3;
  }
  .bookinfo{
    background: #fff;
    letter-spacing: 2px;
    padding-top: 20px;
    position: absolute;
    width: 100%;
    img{
      width: 250rpx;
      height: 250rpx;
    }
    .right_book{
      position: absolute;
      margin-top: -120px;
      padding-left: 120px;
      .title{
        font-size: 16px;
        font-weight: bold;
        margin-bottom: 2px;
      }
      .text_i{
        padding-top: 2px;
        font-size: 16px;
      }
    }
  }
  .rate{
    position: relative;
    display: inline-block;
    span{
      color: #ccc;
    }
    .hollow{
      color:yellow;
      position: absolute;
      display: inline-block;
      top:0;
      left:0;
      width:0;
      overflow:hidden;
    }
    .span-text{
      color: #aaa;
      padding-left: 3px;
      font-size: 14px;
    }
  }
  .updatedchapter{
    position: absolute;
    background: #fff;
    width: 100%;
    height: 50px;
    line-height: 50px;
    font-size: 14px;
    border-top: solid 1px #ccc;
    p{
      float: left;
      padding-left: 10px;
      color: #99CCFF;
      width: 80px;
      span{
        padding-left: 5px;
        border-right: solid 1px #ccc;
      }
    }
    span{
      padding-left: 5px;
      color: #ccc;
    }
    img{
      width: 23rpx;
      height: 25rpx;
      float: right;
      padding-top: 19px;
      padding-right: 10px;
    }
  }
  .jianjie{
    position: absolute;
    margin-top: 50px;
    width: 100%;
    height: 140px;
    background: #fff;
    border-top: solid 1px #ccc;
    .name {
      position: absolute;
      float: left;
      width: 80px;
      padding-left: 20px;
      padding-top: 20px;
      font-size: 18px;
      font-weight: bold;
      span{
        margin-left: -55px;
        border-right: solid 5px #EA5149;
      }
    }
    .jianjie_text{
      font-size: 16px;
      color: #aaa;
      padding-top: 60px;
      padding-left: 10px;
      p{
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        overflow: hidden;
      }
      /*img{*/
        /*width: 23rpx;*/
        /*height: 25rpx;*/
        /*float: right;*/
        /*padding-top: 3px;*/
        /*padding-right:10px;*/
      /*}*/
    }
  }
  .recommend {
    position: absolute;
    width: 100%;
    height: 80px;
    margin-top: 340px;
    background: #fff;
    border-top: solid 1px #ccc;
    .name {
      position: absolute;
      font-size: 18px;
      width: 96px;
      float: left;
      padding-left: 20px;
      padding-top: 20px;
      font-size: 18px;
      font-weight: bold;
      span {
        margin-left: -95px;
        border-right: solid 5px #EA5149;
      }
    }
    .refresh{
      float: right;
      padding-top: 27px;
      font-size: 12px;
      padding-right: 15px;
      color: #aaa;
    }

  }
  .books{
    position: absolute;
    margin-top: 60px;
    background: #fff;
    .hetight_div{
      height: 49px;
    }
    .book-list{
      margin-top: 10px;
      width: 100%;
      img{
        width: 150rpx;
        height: 150rpx;
        border-radius: 10px;
      }
      .title{
        margin-top: -70px;
        padding-left: 80px;
        font-size: 16px;
      }
      .book-chapter{
        padding-top: 5px;
        padding-left: 80px;
        font-size: 14px;
        color: #ccc;
        p{
          margin-top: 10px;
        }
        .list-border{
          padding-top: 20px;
          border-bottom: solid 1px #ccc;
          width: 300px;
        }
      }
    }
  }

  .operation{
    position: fixed;
    width: 100%;
    bottom: 0;
    text-align: center;
    .addbook{
      background: #f0f1f3;
      line-height: 50px;
      font-size: 18px;
      height: 50px;
      float: left;
      width: 50%;
      color: #aaa;
      p{
        float: right;
        padding-right: 40px;
      }
      img{
        width: 40rpx;
        height: 40rpx;
        margin-top: 15px;
        padding-left: 40px;
      }
    }
    .readbook{
      background: #EA5149;
      height: 50px;
      font-size: 18px;
      line-height: 50px;
      color: #fff;
    }
  }
</style>
