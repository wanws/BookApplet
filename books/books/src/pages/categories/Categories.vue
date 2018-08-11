<template>
    <div class="container">
      <div class="header">
        <div class="header_type">
          <p @click="click_hot" v-bind:class="hot_active">热门</p>
          <p @click="click_new">新书</p>
          <p @click="click_over">完结</p>
        </div>
      </div>
      <ul class="books">
        <li @click="clcik_book(book._id)" class="book-list" :key="book.index" v-for="book in books">
          <img mode="aspectFit" :src="book.cover" alt="">
          <div class="title">
            {{book.title}}
          </div>
          <div class="book-chapter">
            <span v-if="book.updated">更新时间:{{book.updated}}</span>
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
  export default {
    data () {
      return {
        res: [],
        name: '', // 类别
        gender: '', // 频道分类
        type: 'hot', // 书籍属性分类
        start: 0, // 分页开始页
        books: [], // 书籍列表
        more: true
      }
    },
    computed: {
      hot_active () {
        return `active`
      }
    },
    mounted () {
      this.books = []
      this.name = this.$root.$mp.query.name
      this.gender = this.$root.$mp.query.gender
      this.bookcategories_title() // 修改标题
      // 请求server
      this.getServerBookType()
    },
    // 触底刷新
    onReachBottom () {
      if (!this.more) {
        // 没有更多了
        return false
      }
      this.start = this.start + 20
      this.getServerBookType()
    },
    onPullDownRefresh: function () {
      wx.stopPullDownRefresh()
    },
    methods: {
      // 点击完结
      click_over () {
        this.type = 'over'
        this.books = []
        this.getServerBookType()
      },
      // 点击新书
      click_new () {
        this.books = []
        this.type = 'new'
        this.getServerBookType()
      },
      // 点击热门标签
      click_hot () {
        this.books = []
        this.type = 'hot'
        this.getServerBookType()
      },
      // 书籍点击跳转
      clcik_book (bookid) {
        console.log('click, ' + bookid)
        wx.navigateTo({
          url: '/pages/detail/main?bookid=' + bookid
        })
      },
      // 请求server
      async  getServerBookType () {
        const data = {
          name: this.name,
          gender: this.gender,
          type: this.type,
          start: this.start
        }
        this.res = get(config.getBookCategoriesUrl, data)
        // console.log(this.res)
        this.res
          .then(value => {
            // console.log(value)
            this.books = this.books.concat(value)
          })
      },
      // 修改标题
      bookcategories_title () {
        wx.setNavigationBarTitle({
          title: this.name
        })
      }
    }
  }
</script>

<style lang="scss">
  body{
    background: #f0f1f3;
  }
.header{
  background: #fff;
  width: 100%;
  height: 50px;
  line-height: 50px;
  .header_type{
    width: 100%;
    p{
      float: left;
      font-size: 16px;
      padding-left: 10px;
    }
    .active{
      color: #EA5149;
    }
  }
}
  .books{
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
