<template>
  <div class="app-layout" v-if="routerAlive">
    <div v-if="isPC">
      <el-config-provider :locale="zhCn">
        <router-view></router-view>
      </el-config-provider>
    </div>
    <div class="mobile" v-else>
      <img src="@/assets/img/login-box-bg.svg" alt="">
      <h3>书缘社</h3>
      <p>当前访问地址为PC端，请使用PC访问</p>
    </div>
  </div>
</template>
<script lang="ts" setup>
import {ref, provide} from 'vue';
import {ElNotification} from 'element-plus';
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'

const routerAlive = ref(true)
const userAgent = navigator.userAgent;
let isPC = ref(true)
// 判断是否为手机设备
if (/(Android|iPhone|iPad|iPod|Mobile)/.test(userAgent)) {
  ElNotification.closeAll()
  isPC.value = false
}
provide("reload", routerAlive)
</script>
<style lang="less">
.app-layout {
  height: 100vh;
  width: 100%;
  overflow: hidden;


  .mobile {
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    text-align: center;
    line-height: 30px;
    transform: translateY(-50%);
    margin-top: 50%;

    img {
      width: 50%;
    }

    a {
      color: #1989fa;
    }
  }
}
</style>
