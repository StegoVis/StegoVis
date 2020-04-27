import Vue from 'vue'
import App from './App.vue'
import store from './store'

import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
Vue.use(ElementUI)

import VueVega from 'vue-vega'
Vue.use(VueVega)

window.baseURL = ""
if (process.env.NODE_ENV === 'production') {
  axios.defaults.baseURL = "http://go-tree.info/stegovis"
  window.baseURL = "http://go-tree.info/stegovis"
}

import axios from 'axios'
import VueAxios from 'vue-axios'

axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*';

Vue.use(VueAxios, axios)

import router from "./router"

Vue.config.productionTip = false

import * as d3 from "d3"
window.d3 = d3

import * as $ from 'jquery'
window.$ = $

import './assets/font/iconfont.css'
//	import the materials icon library
import './assets/icon/icon.css'
import './assets/animation/animate.min.css'

new Vue({
  store,
  router,
  render: h => h(App)
}).$mount('#app')
