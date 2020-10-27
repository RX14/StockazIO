import logger from '@/logging'
import { getOrCreateApp } from '../backend/oauth/oauth.js'

const checkOAuthToken = async ({ store }) => {
  return new Promise(async (resolve, reject) => {
    if (store.getters.getUserToken()) {
      try {
        await store.dispatch('user/loginUser', store.getters.getUserToken())
      } catch (e) {
        logger.default.error(e)
      }
    } else {
      logger.default.info('no user token present in cache')
    }
    resolve()
  })
}

const getAppSecret = async ({ store }) => {
  const { state, commit } = store
  const { oauth } = state
  return getOrCreateApp({ ...oauth, commit })
}

const initializeSomeStuff = async ({ store }) => {
  logger.default.info('Doing preliminary app initialization...')

  if (!store.state.server.serverUrl) {
    // we have several way to guess the API server url. By order of precedence:
    // 1. use the url specified when building via VUE_APP_SERVER_URL
    // 2. use the current url
    let defaultServerUrl = process.env.VUE_APP_SERVER_URL || store.getters['server/defaultUrl']()
    store.commit('server/serverUrl', defaultServerUrl)
  } else {
    // needed to trigger initialization of axios / service worker
    store.commit('server/serverUrl', store.state.server.serverUrl)
  }
  // Fetch server settings
  store.dispatch('server/fetchSettings').finally(() => {
    // Start oauth init
    // let store = this.$store
    // let router = this.$router
    // initializeSomeStuff({ store, router })
  })

  Promise.all([
    // Check token and try to log user if found
    checkOAuthToken({ store }),
    // Try to get or create oauth2 app and token thingy
    getAppSecret({ store })
  ])
    .catch(function (error) {
      logger.default.error('Error while doing initialization', error)
    })
}

export default initializeSomeStuff
