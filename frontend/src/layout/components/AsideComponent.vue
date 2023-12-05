<template>
  <div class="aside-layout">
    <el-menu style="overflow-x:hidden;" :collapse-transition="false" :unique-opened="true"
             :collapse="mainStore.isCollapse" class="el-menu-vertical-demo scroll-bar" :default-active="route.path"
             :router="true">
      <div v-for="(item) in menuList">
        <SubMenu
            v-if="item.name != 'manage'&& item.name!='log' || item.name == 'manage' && privilege<=1 || item.name == 'log' && privilege<=1 "
            :key="item.name"
            :item="item"></SubMenu>
      </div>
    </el-menu>
  </div>
</template>

<script lang="ts" setup>
/* eslint-disable */
import {ref} from 'vue'
import {useRouter, useRoute} from 'vue-router';
import {useMainStore} from '@/store/index'
import SubMenu from './SubMenu.vue';

const mainStore = useMainStore()
const router = useRouter()
const route = useRoute()
const menuList = ref<any>(router.options.routes[0].children)
const localUserData = localStorage.getItem("user_data")
const privilege = parseInt(JSON.parse(localUserData as string)['privilege'])
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
