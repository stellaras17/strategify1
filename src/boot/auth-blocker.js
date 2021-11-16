import { LocalStorage } from "quasar"

export default ({router}) => {
  router.beforeEach((to, from, next) => {
    let checkLoggedIn = LocalStorage.getItem('loggedIn')
    if (!checkLoggedIn && to.path !== '/auth') {
      next('/auth')
    }
    else {
      next()
    }
  })
}
