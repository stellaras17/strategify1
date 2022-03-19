
const routes = [
  {
    path: '/',
    component: () => import('layouts/Layout.vue'),
    children: [
      { path: '', component: () => import('pages/PageStrats.vue') },
      { path: '/orders', component: () => import('pages/PageOrders.vue') },
      { path: '/auth', component: () => import('pages/PageAuth.vue') },
      { path: '/currencies', component: () => import('pages/PageCurrencies.vue') },
      { path: '/hub', component: () => import('pages/PageHub.vue') },
      { path: '/settings', component: () => import('pages/PageSettings.vue') },
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '*',
    component: () => import('pages/Error404.vue')
  }
]

export default routes
