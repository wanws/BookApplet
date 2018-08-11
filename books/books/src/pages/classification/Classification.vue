<template>
  <div class="container">
    <div class="male">
      <p>男生</p>
      <ul>
        <li :key="d.index" v-for="d in data.male" @click="clcik_name('male',d.name)">
          <div class="title">
            {{d.name}}
          </div>
          <p>{{d.bookCount}}本</p>
        </li>
      </ul>
    </div>
    <div class="male">
      <p>女生</p>
      <ul>
        <li :key="d.index" v-for="d in data.female" @click="clcik_name('female',d.name)">
          <div class="title">
            {{d.name}}
          </div>
          <p>{{d.bookCount}}本</p>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
  import {get} from '../../utils'
  import config from '../../config'
  export default {
    data () {
      return {
        res: [],
        data: [] // 保存书籍分类数据
      }
    },
    mounted () {
      this.booktype_title() // 修改标题
      this.getServerBookType() // 请求资源
    },
    methods: {
      // 点击分类
      clcik_name (gender, name) {
        console.log(gender, name)
        wx.navigateTo({
          url: '/pages/categories/main?name=' + name + '&gender=' + gender
        })
      },
      // 请求资源
      async  getServerBookType () {
        const data = {}
        this.res = get(config.getBookTypeUrl, data)
        this.res
          .then(value => {
            // console.log(value)
            this.data = value
          })
      },
      // 修改标题
      booktype_title () {
        wx.setNavigationBarTitle({
          title: '分类'
        })
      }
    }
  }
</script>

<style lang="scss">
  body{
    /*background: #f0f1f3;*/
  }
  .male{
    float: left;
    margin-bottom: 10px;
    p{
      color: #ccc;
      font-size: 14px;
      padding-top: 15px;
      padding-left: 10px;
    }
    ul{
      padding-top: 20px;
      width: 100%;
      li{
        float: left;
        width: 32.8%;
        height: 60px;
        border: solid 1px #f0f1f3;
        .title{
          font-size: 16px;
          line-height: 50px;
          text-align: center;
        }
        p{
          text-align: center;
          padding-top: 20px;
          margin-top: -30px;
        }
      }
    }
  }
</style>
