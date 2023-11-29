import { createApp } from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus'
import { createPinia } from 'pinia'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import DirectiveVue from '@/directive/index'
import router from './router'
import 'element-plus/dist/index.css'
import 'element-plus/theme-chalk/dark/css-vars.css'
import '@/assets/style/element.less'
import '@/assets/style/common.less'

const app = createApp(App)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}
const pinia = createPinia()
const directiveVue = new DirectiveVue();
directiveVue.watermark(app)
// directiveVue.demo(app) //注册多个全局指令

app.use(router).use(ElementPlus).use(pinia).mount('#app')
