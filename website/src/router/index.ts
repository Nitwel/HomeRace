import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router'
import Home from '../views/Home.vue'
import Carts from '../views/Carts.vue'
import Race from '../views/Race.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/carts',
    name: 'Carts',
    component: Carts
  },
  {
    path: '/race',
    name: 'Race',
    component: Race
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
