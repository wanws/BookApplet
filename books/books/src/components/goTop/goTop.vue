<template>
  <div class="goTop">
    <img src='../../../static/image/shangjiantou.png' v-if="goTopShow"   mode="aspectFit" @click="goTop">
  </div>
</template>
<script>
  export default {
    name: 'goTop',
    data () {
      return {
        goTopShow: false
      }
    },
    // 获取滚动条当前位置
    onPageScroll: function (e) {
      // console.log(e)
      if (e.scrollTop > 2000) {
        this.goTopShow = true
      } else {
        this.goTopShow = false
      }
    },
    methods: {
      // 回到顶部
      goTop: function (e) { // 一键回到顶部
        if (wx.pageScrollTo) {
          wx.pageScrollTo({
            scrollTop: 0
          })
        }
      }
    }
  }
</script>

<style lang="scss">
  /* 返回顶部 */
  .goTop{
  img{
    height: 50rpx;
    width: 50rpx;
  }
  position: fixed;
  background: rgba(0,0,0,.3);
  bottom: 50rpx;
  right: 30rpx;
  }
</style>
