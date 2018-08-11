<template>
  <div class="container">

    <div class="header">
      <img @click="login" v-if="userinfo.avatarUrl" :src="userinfo.avatarUrl">
      <div class="username">
        <p @click="login" v-if="userinfo.nickName">{{userinfo.nickName}}</p>
      </div>
    </div>
    <div class="balance">
      <div class="book_left">
        <span>0</span>
        书币
      </div>
      <div class="book_right">
        <span>0</span>
        书卷
      </div>
    </div>
    <ul class="lists">
      <li class="list"><img :src="MeImage.browsing_history">浏览记录</li>
      <li class="list"><img :src="MeImage.qiandao">每日签到 <span>可获得10经验</span></li>
      <li class="list"><img :src="MeImage.jingyan">经验等级 <span>5级</span></li>
    </ul>
    <ul class="lists">
      <li class="list"><img :src="MeImage.message">消息</li>
      <li class="list"><img :src="MeImage.invitation">邀请好友</li>
    </ul>
    <ul class="lists">
      <li class="list"><img :src="MeImage.my_bookcase">我的书架</li>
    </ul>
    <!--获取授权-->
    <div class="btn-open">
      <button class="btn" open-type="getUserInfo" @getuserinfo="doLogin">获取授权</button>
    </div>

  </div>
</template>

<script>
  import {showSuccess, post} from '../../utils'
  import config from '../../config'

  export default {

    data () {
      return {
        userinfo: {
          avatarUrl: '../../../static/image/unlogin.png',
          nickName: '点击登录'
        },
        encryptedData: '',
        MeImage: {}
      }
    },
    onload () {

    },
    mounted () {
      // 一进来看看用户是否授权过
      this.getSetting()
      this.MeImage = config.MeImge
      this.Personal()
    },
    methods: {
      // 修改标题
      Personal: () => {
        wx.setNavigationBarTitle({
          title: '个人中心'
        })
      },
      // 点击登录
      login () {
        console.log('click login')
        let user = wx.getStorageSync('userinfo')
        if (!user) {
          // 一进来看看用户是否授权过
          this.getSetting()
        } else {
          this.userInfo = user
          // console.log(this.userInfo );
        }
      },
      // 检测授权登录
      getSetting () {
        wx.getSetting({
          success: res => {
            if (res.authSetting['scope.userInfo']) {
              wx.getUserInfo({
                success: res => {
                  // 本地存储
                  wx.setStorageSync('userinfo', res.userInfo)
                  // 用户已经授权过
                  this.userinfo = res.userInfo
                  this.encryptedData = res.encryptedData
                  this.getLoginCode()
                  console.log('用户已经授权过')
                }
              })
            } else {
              showSuccess('未授权')
              console.log('用户还未授权过')
            }
          }
        })
      },
      doLogin (e) {
        // console.log(e.mp.detail.rawData)
        if (e.mp.detail.rawData) {
          // 用户按了允许授权按钮
          console.log('用户按了允许授权按钮')
        } else {
          // 用户按了拒绝按钮
          console.log('用户按了拒绝按钮')
        }
      },
      getLoginCode () {
        wx.login({
          success: res => {
            if (res.code) {
              // 发起网络请求
              const user = post(config.loginUrl, {'code': res.code, 'userinfo': this.userinfo, 'encryptedData': this.encryptedData})
              user.then(value => {
                // value.nickName = this.userinfo.nickName
                // 本地存储
                wx.setStorageSync('userinfo', value)
              })
            }
          }
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
    position: relative;
    background: #fff;
    height:60px;
    border-bottom: solid 1px #ccc;
    img{
      float: left;
      width: 70rpx;
      height: 70rpx;
      margin: 20rpx;
      border-radius: 50%;
    }
    .username{
      p{
        line-height: 50px;
        font-size: 14px;
      }
    }

  }
  .balance{
    background: #fff;
    text-align: center;
    height: 50px;
    line-height: 50px;
    font-size: 12px;
    color: #aaa;
    width: 100%;
    span{
      color: black;
    }
    .book_left{
      float: left;
      border-right: solid 1px #ccc;
      width: 50%;
    }
  }
  .lists{
    position: relative;
    margin-top: 10px;
    background: #fff;
    .list{
      font-size: 14px;
      text-align: left;
      border-top: 1px solid #ccc;
      height: 40px;
      line-height: 40px;
      padding-left: 2px;
      img{
        float: left;
        padding-top: 8px;
        padding-right: 10px;
        width: 50rpx;
        height: 50rpx;
        margin: 2rpx;
      }
      span{
        color: #aaa;
        font-size: 10px;
        margin-left: 50%;
      }
    }
  }
  .btn-open{
    height: 100px;
  }
  .btn{
    margin-top: 20px;
    background:#EA5149;
    height: 30px;
    width: 96%;
    line-height: 30px;
    color: #fff;
    font-size: 14px;
    border-radius: 4px;
  }
</style>
