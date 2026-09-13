import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'

// ✅ Element Plus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

window.onerror = function (
  message,
  source,
  lineno,
  colno,
  error
) {
  if (
    message &&
    message.includes(
      'ResizeObserver loop'
    )
  ) {
    return true
  }
}

window.addEventListener(
  'error',
  e => {
    if (
      e.message &&
      e.message.includes(
        'ResizeObserver loop'
      )
    ) {
      e.stopImmediatePropagation()
    }
  }
)

const app = createApp(App)

app.use(router)
app.use(ElementPlus)
// 设置一个请求拦截器处理token
axios.interceptors.request.use(config => {
  const tokenStr = window.sessionStorage.getItem('token')
  if (tokenStr) {
    config.headers.token = tokenStr
  }
  return config
  // 返回请求头
})

// 设置一个响应拦截器处理token是否有效
axios.interceptors.response.use(response => {
  if (response.data.status === 10016 || response.data.status === 10017) {
    window.sessionStorage.removeItem('token')
    router.replace(
      {
        path: '/login'
      }
    )
  }
  return response
})
app.mount('#app')
