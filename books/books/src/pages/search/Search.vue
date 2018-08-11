<template>
  <div class="container">
    <div class="search">
      <form>
        <!--<input type="submit" v-model="key" v-on:input ="bindKeyInput" placeholder="搜索书名或作者">-->
        <input type="submit" v-model="key"  placeholder="搜索书名或作者">
        <img @click="search_click"  mode="aspectFit"  src="../../../static/image/sousuo.png" alt="">
      </form>
    </div>
    <ul class="query_lists" v-if="sub_query">
      <li :key="sub.index" v-for="sub in sub_list" class="query_list" @click="click_query(sub)">{{sub}}</li>
    </ul>
    <div class="top_search">
      <div class="top_on">
        <div class="title">
          热门搜索
        </div>
        <img mode="aspectFit" @click="click_refresh" src="../../../static/image/shuaxin.png" alt="">
      </div>
      <div class="top_center">
        <ul class="top_word_lists">
          <li class="top_word_list" :key="hot.idnex" v-for="hot in hot_res" @click="click_hot_words(hot.word)">{{hot.word}}</li>
        </ul>
      </div>
    </div>
    <div class="search_history">
      <div class="top_on">
        <div class="title">
          搜索历史
        </div>
        <img src="../../../static/image/clear.png" @click="click_clear" alt="">
      </div>
      <div class="history_text">
        <ul >
          <li :key="key.index" @click="click_history_keys(key)" v-for="key in history_keys">{{key}}</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
  import {get} from '../../utils'
  import config from '../../config'
  export default {
    data () {
      return {
        key: '', // 搜索 key 值
        keys: [], // 搜索历史
        history_keys: [],
        sub_list: [], // 搜索值自动补充数据
        sub_query: false, // 搜索值自动补充
        res: {}, // werver 返回得数据
        hot_res: {} // 搜索热词数据
      }
    },
    mounted () {
      this.booksearch_title()
      // 获取搜索热词
      this.getServerHotWords(config.getSearchHptWordsUrl)
      // 获取缓存
      this.getStoSearchrHistory()
    },

    methods: {
      // 点击历史搜索
      click_history_keys (k) {
        this.key = k
        // 搜索
        this.search_click()
      },
      // 获取缓存
      getStoSearchrHistory () {
        this.history_keys = wx.getStorageSync('search_history')
        if (!this.history_keys) {
          this.history_keys = []
        }
      },
      // 点击搜索热词
      click_hot_words (word) {
        this.key = word
        // 搜索
        this.search_click()
      },
      // 点击清楚搜索历史
      click_clear () {
        // 清除本地缓存
        wx.removeStorageSync('search_history')
      },
      // 点击刷新
      click_refresh () {
        console.log('click refresh')
        this.getServerHotWords(config.getSearchHptWordsUrl)
      },
      // 请求server 热词
      async getServerHotWords (url) {
        const data = {}
        this.hot_res = await get(url, data)
        // console.log(this.hot_res)
      },
      // 点击搜索
      search_click () {
        if (this.key) {
          // console.log(this.key)
          // 写入搜索历史缓存
          this.keys = [this.key].concat(this.keys)
          wx.setStorageSync('search_history', this.keys)
          wx.navigateTo({
            url: '/pages/query/main?query=' + this.key
          })
        }
      },
      // // 自动补充点击
      // click_query (q) {
      //   console.log(q)
      //   this.key = q
      // },
      // 监听input键盘输入
      // bindKeyInput (e) {
      //   if (this.key) {
      //     this.getServerQuery(config.getSubQueryUrl)
      //     this.sub_list = this.res
      //     if (this.sub_list) {
      //       this.sub_query = true
      //     }
      //   } else {
      //     this.sub_query = false
      //   }
      // },
      // 请求server 获取自动补充数据
      // async getServerQuery (url) {
      //   const data = {
      //     query: this.key
      //   }
      //   this.res = await get(url, data)
      // },
      // 修改标题
      booksearch_title () {
        wx.setNavigationBarTitle({
          title: '搜索'
        })
      }
    }
  }
</script>

<style lang="scss">
body{
}
  .search{
    input{
      width: 92%;
      color: #aaa;
      height: 20px;
      line-height: 20px;
      font-size: 12px;
      margin-left: 10px;
      margin-top: 10px;
      border-radius: 10px;
      padding-left: 10px;
      background: #f0f1f3;
      border:solid 1px #f0f1f3;
    }
    img{
      float: right;
      width: 20px;
      height: 20px;
      padding-right: 15px;
      margin-top: -25px;
    }
}
.query_lists{
    margin-top: 10px;
     position: fixed;
    width: 100%;
  .query_list{
    font-size: 12px;
    color: #aaa;
    height: 30px;
    line-height: 30px;
    padding-left: 15px;
    border-top: solid 1px #ccc;
  }
}
  .top_search{
    width: 100%;
    padding-top: 20px;
    .top_on{
      font-size: 16px;
      padding-left: 15px;
    }
    img{
      float: right;
      width: 18px;
      height: 18px;
      padding-right: 15px;
      margin-top: -18px;
    }
  }
  .top_center{
    width: 100%;
    .top_word_lists{
      width:90%;
      padding-left: 30px;
      .top_word_list{
        float: left;
        color: #fff;
        height: 25px;
        font-size: 14px;
        line-height: 25px;
        text-align: center;
        border-radius: 15px;
        letter-spacing: 3px;
        margin-left: 10px;
        margin-top: 20px;
        padding-left: 5px;
        padding-right: 5px;
      }
    }
  }
.search_history{
  width: 100%;
  padding-top: 20px;
  float: left;
  .top_on{
    font-size: 16px;
    padding-left: 15px;
  }
  img{
    float: right;
    width: 18px;
    height: 18px;
    padding-right: 15px;
    margin-top: -18px;
  }
  .history_text{
    padding-top: 20px;
    ul li{
      color: #aaa;
      float: left;
      height: 30px;
      font-size: 14px;
      line-height: 30px;
      padding-left: 10px;
      padding-right: 10px;
      margin-left: 10px;
      border-radius: 15px;
      text-align: center;
      border: solid 1px #ccc;
    }
  }

}

// 搜索热词 样式背景色
.top_center  ul li:first-child {
  background-color: #99e084;
  border: solid 1px #99e084;
}
.top_center  ul li:nth-child(2) {
  background-color:#c465dd;
  border: solid 1px #c465dd;
}
.top_center  ul li:nth-child(3) {
  background-color:#99e084;
  border: solid 1px #99e084;
}
.top_center  ul li:nth-child(4) {
  background-color:#f96f4b;
  border: solid 1px #f96f4b;
}
.top_center  ul li:nth-child(5) {
  background-color:#52a2ff;
  border: solid 1px #52a2ff;
}
.top_center  ul li:nth-child(6) {
  background-color:#f67675;
  border: solid 1px #f67675;
}
.top_center  ul li:nth-child(7) {
  background-color:#f0a621;
  border: solid 1px #f0a621;
}
.top_center  ul li:nth-child(8) {
  background-color:#c465dd;
  border: solid 1px #c465dd;
}
.top_center  ul li:nth-child(9) {
  background-color:#52a2ff;
  border: solid 1px #52a2ff;
}
.top_center  ul li:nth-child(10) {
  background-color:#f67675;
  border: solid 1px #f67675;
}
</style>
