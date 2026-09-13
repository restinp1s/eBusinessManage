import axios from 'axios'

const request = axios.create({

  baseURL: 'http://127.0.0.1:5000',

  timeout: 5000

})

// 请求拦截器
request.interceptors.request.use(

  config => {
    const token =
        sessionStorage.getItem('token')

    if (token) {
      config.headers.token = token
    }

    return config
  },

  error => {
    return Promise.reject(error)
  }

)

// 响应拦截器

request.interceptors.response.use(

  response => {
    // 后端token失效处理

    if (
      response.data.status === 1016 ||
            response.data.status === 1017
    ) {
      sessionStorage.removeItem('token')
    }

    return response
  },

  error => {
    console.log(error)

    return Promise.reject(error)
  }

)

export default request
