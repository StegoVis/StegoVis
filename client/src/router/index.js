import Vue from 'vue'
import VueRouter from 'vue-router'
import MainBody from '../views/MainBody.vue'
import Upload from '../views/Upload.vue'

Vue.use(VueRouter)
export default new VueRouter({
	routes: [
		{
			path: "/",
			component: MainBody
		},
		{
			path: "/upload",
			component: Upload
		}
	]
})