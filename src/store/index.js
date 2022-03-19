import Vue from 'vue'
import Vuex from 'vuex'

import strats from './store-strats'
import settings from './store-settings'
import auth from './store-auth'
import orders from './store-orders'
import currencies from './store-currencies'
import users from './store-users'
import hub from './store-hub'

Vue.use(Vuex)

/*
 * If not building with SSR mode, you can
 * directly export the Store instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Store instance.
 */

export default function (/* { ssrContext } */) {
  const Store = new Vuex.Store({
    modules: {
      strats,
      settings,
      auth,
      orders,
      currencies,
      users,
      hub
    },

    // enable strict mode (adds overhead!)
    // for dev mode only
    strict: process.env.DEBUGGING
  })

  return Store
}
