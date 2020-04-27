import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
  	displayMode: 'vis',
    selectedItem: null,
    loading: false
  },
  mutations: {
    ['UPDATE_DISPLAY_MODE'] (state, displayMode) {
      state.displayMode = displayMode
    },
    ['UPDATE_SELECTED_ITEM'] (state, selectedItem) {
      state.selectedItem = selectedItem
    },    
    ['UPDATE_LOADING_MODE'] (state, loading) {
      state.loading = loading
    }
  },
  actions: {

  }
})
