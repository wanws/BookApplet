import Vue from 'vue'
import App from './App'

Vue.config.productionTip = false

const app = new Vue(App)
app.$mount()

export default {
  config: {
    pages: ['^pages/books/main', 'pages/classification/main', 'pages/search/main', 'pages/me/main'],
    'window': {
      'navigationBarBackgroundColor': '#EA5149',
      'navigationBarTextStyle': 'light',
      'navigationBarTitleText': '免费图书阅读',
      'backgroundTextStyle': 'light'
    },
    'tabBar': {
      selectdcolor: '#EA5149',
      'list': [
        {
          pagePath: 'pages/books/main',
          text: '书架',
          iconPath: 'static/image/book.png',
          selectedIconPath: 'static/image/book-active.png'
        },
        {
          pagePath: 'pages/classification/main',
          text: '分类',
          iconPath: 'static/image/classification.png',
          selectedIconPath: 'static/image/classification-active.png'
        },
        {
          pagePath: 'pages/search/main',
          text: '发现',
          iconPath: 'static/image/search.png',
          selectedIconPath: 'static/image/search-active.png'
        },
        {
          pagePath: 'pages/me/main',
          text: '我',
          iconPath: 'static/image/me.png',
          selectedIconPath: 'static/image/me-active.png'
        }
      ]
    }
  }
}
