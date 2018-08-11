import Vue from 'vue'
import Categories from './Categories'

const app = new Vue(Categories)
app.$mount()

export default {
  config: {
    onReachBottomDistance: 1000
  }
}
