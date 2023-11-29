<template>
  <div class="aside-layout">
    <el-menu style="overflow-x:hidden;" :collapse-transition="false" :unique-opened="true"
      :collapse="mainStore.isCollapse" class="el-menu-vertical-demo scroll-bar" :default-active="route.path"
      :router="true">
      <SubMenu v-for="(item) in menuList" :key="item.name" :item="item"></SubMenu>
    </el-menu>
  </div>
</template>

<script lang="ts" setup>
/* eslint-disable */
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router';
import { useMainStore } from '@/store/index'
import SubMenu from './SubMenu.vue';
const mainStore = useMainStore()
const router = useRouter()
const route = useRoute()
const menuList = ref<any>(router.options.routes[0].children)
// const formatRouter = (arr: any) => {
//   arr.forEach((element: any) => {
//     if (element.children && element.children.length > 0) {
//       formatRouter(element.children)
//     }
//     console.log(element);
//     if(!element.hidden){

//     }
//   });
// }
// formatRouter(router.options.routes[0].children)


</script>

<style lang="less" scoped>
.el-menu-vertical-demo {
  height: 100vh;
  overflow-y: auto;

  .menu-title {
    margin-right: 20px;
  }
}
</style>
