<template>
    <div class="container">
      <div class="header">
        <div class="title">
          {{title}}
        </div>
        <div class="right_desc">
          <img mode="aspectFit" @click="click_desc"  :src="desc_src.src">
        </div>
      </div>
      <ul class="lists">
        <li class="list" @click="click_list_chapter(book.chapterLink )" :key="book.index" v-for="book in books"><span>{{index+1}}. </span>{{book.chapterTile}}</li>
        <div class="text-footer" v-if="more">
          没有更多了
        </div>
      </ul>
    </div>
</template>

<script>
  import config from '@/config'
  import {get, showLoadings, showModalLogin} from '../../utils'
  const Base64 = require('js-base64').Base64
  export default {
    data () {
      return {
        bookid: '', // 书籍id
        title: '', // 书籍title
        page: 1, // 分页控制
        userinfo: [], // 用户信息
        books: [], // 书籍章节
        more: true, // 章节加载控制
        desc_src: { // 排序
          src: '../../../static/image/shengxu.png',
          active: true
        }
      }
    },
    mounted () {
      this.bookid = this.$root.$mp.query.bookid
      this.title = this.$root.$mp.query.title
      // 修改标题
      this.booksection()
      // 获取用户信息
      this.userinfo = wx.getStorageSync('userinfo')
      this.page = 1
      this.books = []
      // 请求server
      this.getServerSection()
    },
    // 触底刷新
    onReachBottom () {
      if (!this.more) {
        // 没有更多了
        return false
      }
      this.page = this.page + 1
      this.getServerSection()
    },
    onPullDownRefresh: function () {
      wx.stopPullDownRefresh()
    },
    onLoad () {
      // 加载中
      showLoadings()
    },

    methods: {
      // 验证用户是否登录
      is_userinfo () {
        if (this.userinfo === '') {
          console.log('userinfo null')
          showModalLogin()
        } else {
          return true
        }
      },
      // 点击章节
      click_list_chapter (link) {
        if (this.is_userinfo()) {
          console.log('click  link:' + link)
          wx.navigateTo({
            url: '/pages/content/main?title=' + this.title + '&link=' + link
          })
        }
      },
      // 点击排序
      click_desc () {
        console.log('click desc')
        if (this.desc_src.active) {
          this.desc_src.src = '../../../static/image/jiangxu.png'
          this.desc_src.active = false
        } else {
          this.desc_src.src = '../../../static/image/shengxu.png'
          this.desc_src.active = true
        }
      },
      // 请求server
      async getServerSection () {
        this.more = true
        const header = {
          'content-type': 'application/json',
          'Authorization': 'Basic' + ' ' + Base64.encode(this.userinfo.token + ':password')
        }
        const data = {
          bookid: this.bookid,
          page: this.page
        }
        const books = await get(config.sectionUrl, data, header)
        this.books = this.books.concat(books)
        if (books.length < 50 && this.page > 0) {
          this.more = false
        }
        // console.log(books)
      },
      // 修改标题
      booksection () {
        wx.setNavigationBarTitle({
          title: '目录'
        })
      }
    },
    created () {
    }
  }
</script>

<style lang="scss">
  .header{
    letter-spacing: 2px;
    position: absolute;
    width: 100%;
    height: 50px;
    line-height: 50px;
    .title{
      float: left;
      letter-spacing: 5px;
      color: #EA5149;
      padding-left: 10px;
      font-size: 18px;
      font-weight: bold;
    }
    .right_desc{
      float: right;
      img{
        margin-top: 10px;
        padding-right: 10px;
        width: 60rpx;
        height: 60rpx;
      }
    }
  }
  .lists{
    position: absolute;
    padding-top: 60px;
    width: 100%;
    .list{
      color: #aaa;
      height: 50px;
      line-height: 50px;
      font-size: 16px;
      padding-left: 5px;
      display: -webkit-box;
      -webkit-line-clamp: 1;
      -webkit-box-orient: vertical;
      overflow: hidden;
      border-top: solid 1px #ccc;
    }
  }
  .text-footer{
    text-align: center;
    color: #aaa;
    font-size: 12px;
  }

</style>
