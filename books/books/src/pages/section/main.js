import Vue from 'vue'
import section from './Section'

const app = new Vue(section)
app.$mount()

export default {
  config: {
    onReachBottomDistance: 1000
  }
}
