import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'
import server from './server'
import user from './user'
import oauth from './oauth'
import preloads from './preloads'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    server,
    user,
    oauth,
    preloads
  },
  plugins: [
    createPersistedState({
      key: 'oauth',
      paths: ['oauth']
    }),
    createPersistedState({
      key: 'server',
      paths: ['server.serverUrl']
    })
  ]
})
