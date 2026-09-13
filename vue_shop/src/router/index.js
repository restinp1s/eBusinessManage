import { createRouter, createWebHashHistory } from 'vue-router'
import login from '../components/UserLogin.vue'
import '../assets/css/global.css'
import Home from '../components/UserHome.vue'
import UWelcome from '../components/UWelcome.vue'
import UserList from '../components/user/UserList.vue'
import PowerMenu from '../components/power/PowerMenu.vue'
import PowerRole from '../components/power/PowerRole.vue'
import GoodSort from '../components/goods/GoodSort.vue'
import GoodAttr from '../components/goods/GoodAttr.vue'
import GoodList from '../components/goods/GoodList.vue'
import GoodAdd from '../components/goods/GoodAdd.vue'
import OrderList from '../components/order/OrderList.vue'
import DataList from '../components/data/DataList.vue'

const routes = [
  {
    path: '/login',
    component: login
  },
  {
    path: '/home',
    component: Home,
    redirect: 'welcome',
    children: [
      {
        path: '/welcome',
        component: UWelcome
      },
      {
        path: '/user_list',
        component: UserList
      },
      {
        path: '/permission_list',
        component: PowerMenu
      },
      {
        path: '/author_list',
        component: PowerRole
      },
      {
        path: '/psort_list',
        component: GoodSort
      },
      {
        path: '/product_list',
        component: GoodAttr
      },
      {
        path: '/goods_list',
        component: GoodList
      },
      {
        path: '/add_goods',
        component: GoodAdd
      },
      {
        path: '/order_list',
        component: OrderList
      },
      {
        path: '/data_list',
        component: DataList
      }
    ]
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router

router.beforeEach((to, from, next) => {
  if (to.path === '/login') return next()
  const tokenStr = window.sessionStorage.getItem('token')
  if (!tokenStr) return next('/login')
  next()
})
