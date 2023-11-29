<template>
  <el-container class="layout-container-demo" style="height: 100vh">
    <el-aside :width="mainStore.isCollapse ? '64px' : '200px'">
      <el-scrollbar>
        <aside-component></aside-component>
      </el-scrollbar>
    </el-aside>
    <el-container>
      <el-header>
        <div class="toolbar">
          <header-component></header-component>
        </div>
      </el-header>

      <el-main>
        <el-scrollbar v-if="userData.account" v-watermark="userData.account + '-' + userData.nickname">
          <router-view v-slot="{ Component }">
            <el-collapse-transition>
              <component :is="Component" :key="routeKey" />
            </el-collapse-transition>
          </router-view>
        </el-scrollbar>
      </el-main>
    </el-container>
  </el-container>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { ElNotification, ElLoading } from 'element-plus';
import { useRoute, useRouter } from 'vue-router';
import AsideComponent from './components/AsideComponent.vue'
import HeaderComponent from './components/HeaderComponent.vue'
import { useMainStore } from '@/store';
const route = useRoute()
const router = useRouter()
const mainStore = useMainStore()
const routeKey = route.name
let userData = ref({ nickname: "", account: "", id:0, gender:"", age: 0 })
const loading = ElLoading.service({
  lock: true,
  text: '界面加载中，请稍候...',
  background: 'rgba(0, 0, 0, 0.7)',
})
setTimeout(() => {
  const user_data = localStorage.getItem("user_data")
  userData.value = user_data && user_data !== 'undefined' ? JSON.parse(user_data as string) : { nickname: "", account: "" , id:0, gender:"", age: 0 }
  loading.close()
  console.log(user_data)
  console.log(userData.value.account)
  if (!userData.value.account) {
    ElNotification({
      title: '登录信息丢失',
      message: '登录用户信息失效，请重新登录',
      type: 'error',
    })
    router.push({ path: "/login" })
  }
}, 500);
</script>

<style scoped></style>
