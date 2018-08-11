<template>
    <div class="container">
      <div class="statement">
        <p>本程序仅提供搜索引擎服务, 请支持正版!</p>
      </div>
      <ul class="books">
        <li @click="clcik_book(book.id)" class="book-list" :key="book.index" v-for="book in res">
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
    import config from '../../config'
    import {get} from '../../utils'

    export default {
      data () {
        return {
          res: '', // server 返回值
          query: '' // 搜索值
        }
      },
      mounted () {
        this.query = this.$root.$mp.query.query

        // 请求server 端数据
        this.is_query_null()
        // 修改标题
        this.bookquery()
      },
      methods: {
        // 判断query是否为空
        is_query_null () {
          if (this.query !== '') {
            // 请求server
            this.getServerSearchQuery()
          }
        },
        // 请求 server
        async getServerSearchQuery () {
          const data = {
            query: this.query
          }
          this.res = await get(config.getSearchQueryUrl, data)
          // console.log(this.res)
        },
        // 书架点击跳转
        clcik_book (bookid) {
          console.log('click, ' + bookid)
          wx.navigateTo({
            url: '/pages/detail/main?bookid=' + bookid
          })
        },
        // 修改标题
        bookquery () {
          wx.setNavigationBarTitle({
            title: this.query
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
