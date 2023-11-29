const {
  defineConfig
} = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  lintOnSave: false,
  devServer: {
    // 端口号
    port: 8001,
    // 配置不同的后台API地址
    proxy: {
    '/api': {
        target: 'http://10.192.187.233:8000/api/',
        //ws: true,
        changeOrigin: true,
        pathRewrite: {
          '^/api': ''
        }
    }
    },
  }
})