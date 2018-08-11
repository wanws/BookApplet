<template>
  <div class="contatiner" :style="style_bg">
    <div class="title">
      {{content.chapterTile}}
    </div>
    <div class="content" @click="click_content_text" :style="size_style">
      <pre>
        <p :key="content.chapterText.index" v-for="text in content.chapterText">&nbsp;&nbsp;{{text}}</p>
      </pre>
    </div>
    <div class="footer">
      <div class="on-text" @click="click_on">
        上一章
      </div>
      <div class="down-text" @click="click_down">
        下一章
      </div>
    </div>
    <div class="setting" v-if="setting">
      <div class="upper">
        <div class="on_" @click="click_on">
          上一章
        </div>
        <div class="down_" @click="click_down">
          下一章
        </div>
      </div>
      <div class="lower">
        <div class="general_setting" @click="directory_click">
          <img mode="aspectFit"  src="../../../static/image/directory.png"   alt="">
          <span>目录</span>
        </div>
        <div class="general_setting" @click="font_Aa_click">
          <img   mode="aspectFit" src="../../../static/image/font-Aa.png"   alt="">
          <span>设置</span>
        </div>
        <div class="general_setting" @click="shujia_click">
          <img   mode="aspectFit"  src="../../../static/image/shujia.png"  alt="">
          <span>书架</span>
        </div>
        <div class="general_setting" @click="feedback_click">
          <img  mode="aspectFit" src="../../../static/image/feedback.png"    alt="">
          <span>反馈</span>
        </div>
      </div>
    </div>
    <div class="font_setting" v-if="size_setting">
      <div class="header">
        <p>设置</p><img mode="aspectFit" src="../../../static/image/close.png" @click="close_size_setting"   alt="">
      </div>
      <div class="font_size">
        <p>字号<span>{{size}}</span></p>
        <p class="size_seeting" @click="click_min">小</p>
        <p class="size_seeting" @click="click_max">大</p>
      </div>
      <div class="theme">
        <p>主题</p>
        <ul class="theme_lists">
          <li  class="theme_list_default" @click="click_bg_default"></li>
          <li  class="theme_list_white"  @click="click_bg_white"></li>
          <li  class="theme_list_green"  @click="click_bg_green"></li>
          <li  class="theme_list_blue"  @click="click_bg_blue"></li>
          <li  class="theme_list_light_green"  @click="click_bg_light_green"></li>
          <li  class="theme_list_pink"  @click="click_bg_pink"></li>
          <li  class="theme_list_black"  @click="click_bg_black"></li>
          <li  class="theme_list_brown"  @click="click_bg_brown"></li>
        </ul>
      </div>
    </div>
    <go-top></go-top>
  </div>
</template>

<script>
  import config from '@/config'
  import {get, showSuccess} from '../../utils'
  import goTop from '../../components/goTop/goTop'
  const Base64 = require('js-base64').Base64
export default {
    data () {
      return {
        title: '', // 书籍名称
        link: '', // 书籍当前章节链接
        userinfo: [],
        content_text_on: [], // 上一章内容
        content: [], // 当前章节内容
        content_text_down: [], // 下一章内容
        setting: false, // 设置
        size_setting: false,
        size: 16, // 字体大小
        body_bg: '#e9dec0', // 主题背景色
        font_color: 'black', // 字体颜色
        book_content: {} // 章节缓存信息
      }
    },
    mounted () {
      this.link = this.$root.$mp.query.link
      this.title = this.$root.$mp.query.title
      this.bookcontenttitle()
      // 获取用户信息
      this.userinfo = wx.getStorageSync('userinfo')
      // 请求 server
      this.getServerContent()
    },
    components: {
      goTop
    },
    computed: {
      size_style () {
        return `font-size:${this.size}px;color:${this.font_color}`
      },
      style_bg () {
        return `background-color: ${this.body_bg};`
      }
    },
    methods: {
      // 目录点击
      directory_click () {
        console.log('click directory')
        wx.reLaunch({
          url: '/pages/section/main?bookid=' + this.content.bookinfo_id + '&title=' + this.title
        })
      },
      // 字体设置点击
      font_Aa_click () {
        console.log('click font_Aa')
        this.setting = false
        this.size_setting = true
      },
      // 书架点击
      shujia_click () {
        console.log('click shujia')
        wx.switchTab({
          url: '/pages/books/main'
        })
      },
      // 反馈
      feedback_click () {
        console.log('click feedback')
      },
      // 回到顶部
      goTop: function (e) { // 一键回到顶部
        if (wx.pageScrollTo) {
          wx.pageScrollTo({
            scrollTop: 0
          })
        }
      },
      // 点击屏幕内容页面
      click_content_text () {
        console.log('click text')
        if (!this.size_setting) {
          if (this.setting) {
            this.setting = false
          } else {
            this.setting = true
          }
        }
      },
      // 点击上一章
      click_on () {
        console.log('click on')
        if (this.content_text_on.length === 0) {
          showSuccess('没有上一章了')
        } else {
          this.content_text_down = this.content
          this.link = this.content_text_on.chapterLink
          this.getServerContent() // 请求服务器
          this.setting = false // 修改设置页面显示
          this.goTop() // 返回顶部
        }
      },
      // 点击下一章
      click_down () {
        console.log('click down')
        if (this.content_text_down.length === 0) {
          showSuccess('已经是最后一章了')
        } else {
          this.content_text_on = this.content
          this.link = this.content_text_down.chapterLink
          this.getServerContent()
          this.setting = false
          this.goTop()
        }
      },
      // 请求 server
      async getServerContent () {
        const header = {
          'content-type': 'application/json',
          'Authorization': 'Basic' + ' ' + Base64.encode(this.userinfo.token + ':password')
        }
        const data = {
          query: this.link
        }
        const res = await get(config.contentUrl, data, header)
        this.content = res.content_text // 当前内容
        this.content_text_on = res.content__on_down.on_book // 上一张内容
        this.content_text_down = res.content__on_down.down_book // 下一张内容
        // 缓存当前章节
        this.svecontent()
      },
      // 将当前章节缓存
      svecontent () {
        this.book_content = {
          bookid: this.content.bookinfo_id,
          title: this.title,
          content: this.content
        }
        wx.setStorageSync(this.content.bookinfo_id, this.book_content)
      },
      // 修改标题
      bookcontenttitle () {
        wx.setNavigationBarTitle({
          title: this.title
        })
      }, // 点击主题颜色
      click_bg_default () {
        this.body_bg = '#e9dec0'
        this.font_color = 'black'
      },
      click_bg_white () {
        this.body_bg = '#f8f8f8'
        this.font_color = 'black'
      },
      click_bg_green () {
        this.body_bg = '#d8ecc9'
        this.font_color = 'black'
      },
      click_bg_pink () {
        this.body_bg = '#f6d9de'
        this.font_color = 'black'
      },
      click_bg_blue () {
        this.body_bg = '#22455b'
        this.font_color = '#f8f8f8'
      },
      click_bg_light_green () {
        this.body_bg = '#e7f0db'
      },
      click_bg_black () {
        this.body_bg = 'black'
        this.font_color = '#f8f8f8'
      },
      click_bg_brown () {
        this.body_bg = '#463434'
        this.font_color = '#f6d9de'
      },
      // 点击关闭字体设置
      close_size_setting () {
        this.size_setting = false
      },
      // 字体设置点击小
      click_min () {
        this.size -= 1
      },
      // 字体设置点击大
      click_max () {
        this.size += 1
      }
    }
  }
</script>

<style lang="scss">
  html {
    -webkit-text-size-adjust: 100%;
    font-family: "miui", "Helvetica Neue",Helvetica,STHeiTi,sans-serif;
    -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
  }
  body {
    background: #e9dec0;
  }
  .title {
    padding: 10px 0px 0px 10px;
    font-size: 15px;
    color: #a89577;
  }
  .content {
    font-size: 16px;
    letter-spacing: 3px;
    p{
      padding-top: 10px;
      padding-right: 10px;
    }
  }
  .footer{
    height: 20px;
    width: 100%;
    font-size: 12px;
    line-height: 20px;
    text-align: center;
    padding: 30px 0 30px 0px;
    .on-text{
      float: left;
      width: 100px;
      color: black;
      background: #fff;
      margin-left: 50px;
      border: solid 1px #fff;
    }
    .down-text{
      float: right;
      width: 150px;
      color: #fff;
      background: #EA5149;
      margin-right: 50px;
      border: solid 1px #EA5149;
    }
  }
  .setting{
    position: fixed;
    width: 100%;
    bottom: 0;
    background-color: rgba(255,255,255,0.95);
    .upper {
      width: 100%;
      text-align: center;
      color: #aaa;
      font-size: 12px;
      height: 50px;
      line-height: 50px;
      letter-spacing: 3px;
      border-bottom: solid 1px #ccc;
      .on_ {
        width: 50%;
        float: left;
        border-right: solid 1px #ccc;
      }
    }
    .lower {
      width: 100%;
      font-size: 14px;
      text-align: center;
      img{
        height: 30rpx;
        width: 30rpx;
        padding-left: 40px;
        padding-bottom: 5px;
      }
      .general_setting{
        padding-top: 15px;
        width: 25%;
        float: left;
        color: #aaa;
      }
    }
  }
.font_setting{
  color: #aaa;
  width: 100%;
  bottom: 0;
  position: fixed;
  font-size: 14px;
  background-color: rgba(255,255,255,0.95);
  .header{
    height: 40px;
    width: 100%;
    line-height: 40px;
    padding-left: 10px;
    border-bottom: solid 1px #ccc;
    img{
      float: right;
      width: 15px;
      height: 15px;
      padding-right: 20px;
      margin-top: -27px;
    }
  }
  .font_size{
    padding-top: 10px;
    p:first-child{
      float: left;
      width: 30%;
      padding-left: 15px;
      span{
        padding-left: 10px;
      }
    }
    .size_seeting{
      width: 80px;
      height: 20px;
      float: left;
      line-height: 20px;
      text-align: center;
      border:solid 1px #ccc;
      border-radius: 5px;
      margin-left: 30px;
    }
  }
  .theme{
    float: left;
    padding-top: 10px;
    padding-left: 15px;
    margin-bottom: 10px;
    .theme_lists{
      margin-top: -16px;
      padding-left: 50px;
      .theme_list_default{
        float: left;
        width: 16px;
        height: 16px;
        background: #e9dec0;
        border-radius: 50%;
        margin-left: 20px;
        border: solid 1px #e9dec0;
      }
      .theme_list_white{
        float: left;
        width: 16px;
        height: 16px;
        background: #f8f8f8;
        margin-left: 20px;
        border: solid 1px #f8f8f8;
        border-radius: 50%;
      }
      .theme_list_green{
        float: left;
        width: 16px;
        height: 16px;
        background: #d8ecc9;
        margin-left: 20px;
        border: solid 1px #d8ecc9;
        border-radius: 50%;
      }
      .theme_list_blue{
        float: left;
        width: 16px;
        height: 16px;
        background: #22455b;
        margin-left: 20px;
        border: solid 1px #22455b;
        border-radius: 50%;
      }
      .theme_list_light_green{
        float: left;
        width: 16px;
        height: 16px;
        background: #e7f0db;
        margin-left: 20px;
        border: solid 1px #e7f0db;
        border-radius: 50%;
      }
      .theme_list_pink{
        float: left;
        width: 16px;
        height: 16px;
        background: #f6d9de;
        margin-left: 20px;
        border: solid 1px #f6d9de;
        border-radius: 50%;
      }
      .theme_list_black{
        float: left;
        width: 16px;
        height: 16px;
        background: black;
        margin-left: 20px;
        border: solid 1px black;
        border-radius: 50%;
      }
      .theme_list_brown{
        float: left;
        width: 16px;
        height: 16px;
        background:  #463434;
        margin-left: 20px;
        border: solid 1px #463434;
        border-radius: 50%;
      }
    }
  }
}

</style>
