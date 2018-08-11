<template>
  <div class="container">
    <div class="statement">
      <p>本程序仅提供搜索引擎服务, 请支持正版!</p>
    </div>
    <div class="signin">
      已连续签到<span>0</span>天,再签<span>7</span>天可获得经验礼包
      <button @click="clicksigin">立即签到</button>
    </div>
    <div class="recommend" :key="rec.index" v-for="rec in recommend" @click="click_recommend(rec.bookid)">
      <p>推荐:</p>
      <span>{{rec.rec_lang}}</span>
      <img mode="aspectFit" src="../../../static/image/jiantou.png" alt="">
    </div>
    <ul class="books">
      <li @click="clcik_book(book.id)" class="book-list" :key="book.index" v-for="book in bookcase">
        <img mode="aspectFit" :src="book.cover" alt="">
        <div class="title">
          {{book.title}}
        </div>
        <div class="book-chapter">
          <span>更新时间:{{book.updated}}</span>
          <p>{{book.lastChapter}}</p>
          <div class="list-border">
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
  import {get} from '../../utils'
import config from '../../config'
const Base64 = require('js-base64').Base64
  export default {
    data () {
      return {
        // 本地存储书架
        bookcase: {},
        // 本地用户信息
        userinfo: [],
        // 推荐
        recommend: []
      }
    },
    mounted () {

    },
    onLoad () {
      // 获取用户信息
      this.userinfo = wx.getStorageSync('userinfo')
      // 请求server首页api数据
      this.getBookIndex()
    },
    methods: {
      // 读取本地书籍缓存
      getStorBooks () {
        this.recommend = wx.getStorageSync('recommend')
        this.bookcase = wx.getStorageSync('books')
      },
      // 请求server首页api数据
      async getBookIndex () {
        const header = {
          'content-type': 'application/json',
          'Authorization': 'Basic' + ' ' + Base64.encode(this.userinfo.token + ':password')
        }
        const data = {}
        if (this.userinfo) {
          const bookindex = await get(config.UserindexUrl, data, header)
          this.setdata(bookindex)
        } else {
          const bookindex = await get(config.indexUrl, data, header)
          this.setdata(bookindex)
        }
        // 写入本地缓存
        wx.setStorageSync('books', this.bookcase)
      },
      // 保存从server端返回得数据
      setdata (bookindex) {
        this.bookcase = bookindex.books
        this.recommend = bookindex.recommend
      },
      // 签到跳转
      clicksigin () {
        console.log('click 立即签到')
      },
      // 书架点击跳转
      clcik_book (bookid) {
        console.log('click, ' + bookid)
        wx.navigateTo({
          url: '/pages/detail/main?bookid=' + bookid
        })
      },
      // 推荐跳转
      click_recommend (bookid) {
        console.log('click 推荐, ' + bookid)
        wx.navigateTo({
          url: '/pages/detail/main?bookid=' + bookid
        })
      }
    }
  }
</script>

<style lang="scss">
  .statement{
    height: 30px;
    font-size: 10px;
    background: #eee;
    line-height: 30px;
    p{
      text-align: center;
      color: #aaa;
    }
  }
  .signin{
    position: absolute;
    padding-left: 10px;
    height: 80px;
    width: 100%;
    font-size: 12px;
    line-height: 80px;
    color: #aaa;
    border-bottom: solid 1px #ccc;
    border-top: solid 1px #ccc;
    letter-spacing: 1px;
    span{
      color: red;
      font-size: 14px;
      font-weight: bold;
    }
    button{
      margin-top: 25px;
      margin-right: 20px;
      float: right;
      width: 90px;
      font-size: 12px;
      background: #EA5149;
      color: #fff;
    }
  }
  .recommend{
    position: absolute;
    width: 100%;
    height: 40px;
    margin-top: 80px;
    line-height:40px;
    border-bottom: solid 1px #ccc;
    p{
      margin-left: 25px;
      float: left;
      font-size: 16px;
      color: #EA5149;
      font-weight: bold;
      height: 40px;
    }
    span{
      float: left;
      padding-left: 10px;
      font-size: 16px;
    }
      img{
        width: 23rpx;
        height: 25rpx;
        float: right;
        padding-top: 16px;
        padding-right: 10px;
      }

  }
  .books{
    position: absolute;
    margin-top: 120px;
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
</style>
