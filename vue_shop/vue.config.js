const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      '/user': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true
      },
      '/category_list': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true
      },

      '/category': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true
      },
      '/goods': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true
      },
      // 图片上传接口
      '/upload_img': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true
      }
    },
    client: {

      overlay: false

    }
  }
})
// proxy作用是解决 Vue 前端访问 Flask 后端时的跨域问题
