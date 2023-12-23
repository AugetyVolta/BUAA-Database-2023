<script lang="ts" setup>
import {ref, watch,} from 'vue';
import {useRouter, useRoute} from 'vue-router';
import {ElMessageBox, ElMessage} from 'element-plus'
import {useDark, useFullscreen} from '@vueuse/core';
import {useMainStore} from '@/store/index';
/* eslint-disable */
const mainStore = useMainStore()
const isDark = useDark()
const router = useRouter()
const outLogin = (): void => {
  ElMessageBox.confirm(
      '是否注销本次登录并清空所有登录信息?',
      '注销提示',
      {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning',
      }
  ).then(() => {
    router.push({path: "/login"})
    ElMessage({
      type: 'success',
      message: '登录信息已注销，已完成退出',
    })
    let removeItemList = ["user_data", "token"]
    removeItemList.forEach((item: string) => {
      localStorage.removeItem(item)
    })
  }).catch(() => {})
}
const {toggle,} = useFullscreen()
const route = useRoute()
let userData = ref({nickname: "XXXX", account: "XXXX"})
if (userData.value.nickname == 'XXXX') {
  setTimeout(() => {
    const userinfo = localStorage.getItem("user_data")
    userData.value = userinfo && userinfo !== 'undefined' ? JSON.parse(userinfo as string) : {
      nickname: "XXXX",
      account: "XXXX"
    }
  }, 200);
}

interface meat {
  path: string,
  title: string
}

let pathArr: meat[] = []
route.matched.forEach((item: any) => {
  let meta = item.meta
  let path: string = item.path
  if (meta.parentPath && meta.parent) {
    pathArr.push({path: meta.parentPath, title: meta.parent})
  }
  pathArr.push({path: path, title: meta.title})
})

let routerArr = ref<any>(pathArr)

watch(route, (next, _) => {
  let tempArr: meat[] = []
  next.matched.forEach((item: any) => {
    let meta = item.meta
    let path: string = item.path
    if (meta.parentPath && meta.parent) {
      tempArr.push({path: meta.parentPath, title: meta.parent})
    }
    tempArr.push({path: path, title: meta.title})
  })
  routerArr.value = tempArr
})


</script>
<template>
  <div class="header-layout">
    <div class="header-left-layout">
      <div class="trigger" @click="mainStore.onTrigger">
        <el-icon class="icon" v-if="mainStore.isCollapse">
          <Expand/>
        </el-icon>
        <el-icon class="icon" v-else>
          <Fold/>
        </el-icon>
      </div>
      <div>
        <el-breadcrumb separator-icon="ArrowRight">
          <transition-group name="list">
            <el-breadcrumb-item v-for="item in routerArr" :key="item.path" :to="item.path">
              {{ item.title }}
            </el-breadcrumb-item>
          </transition-group>
        </el-breadcrumb>
      </div>
    </div>
    <div class="header-right-layout">
      <el-button class="right-icon" icon="User" @click="router.push({ path: '/user-center' })">
        {{ userData.account }} / {{ userData.nickname }}
      </el-button>
<!--      <el-icon @click="toggle" class="icon right-icon">-->
<!--        <FullScreen/>-->
<!--      </el-icon>-->
      <el-switch class="right-icon" size="large" @change="mainStore.changeTheme()"
                 style="--el-switch-on-color: #2c2c2c; --el-switch-off-color: #f2f2f2;" v-model="isDark" inline-prompt
                 active-action-icon="Moon" inactive-action-icon="Sunny"/>
      <el-icon @click="outLogin" class="icon right-icon">
        <SwitchButton/>
      </el-icon>
    </div>
  </div>
</template>
<style lang='less' scoped>
.list-move,
  /* 对移动中的元素应用的过渡 */
.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}

.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

/* 确保将离开的元素从布局流中删除
  以便能够正确地计算移动的动画。 */
.list-leave-active {
  position: absolute;
}

.header-layout {
  display: flex;
  justify-content: space-between;
  align-items: center;
  line-height: 50px;
  --el-table-border-color: var(--el-border-color-lighter);
  --el-table-border: 1px solid var(--el-table-border-color);
  border-bottom: var(--el-table-border);
  padding: 0 10px;

  .header-left-layout {
    display: flex;
    align-items: center;
    text-align: left;

    .trigger {
      margin-right: 30px;
    }
  }


  .icon {
    font-size: 25px;
    cursor: pointer;
    line-height: 80px;
    vertical-align: middle;

    &:hover {
      color: #409eff;
    }
  }

  .right-icon {
    cursor: pointer;
    margin: 0 20px;
  }
}
</style>