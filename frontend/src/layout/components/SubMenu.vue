<script lang="ts" setup>
/* eslint-disable */
import { RouteRecordRaw } from 'vue-router'
import SubMenu from './SubMenu.vue';
defineProps({
  item: {
    require: true,
    default: () => { return {} as RouteRecordRaw }
  },
})
</script>
<template>
  <el-sub-menu :index="item.name" v-if="item.children && item.children.length > 0">
    <template #title>
      <el-icon>
        <component :is="item?.meta?.icon" />
      </el-icon>
      <span class="menu-title">{{ item?.meta?.title }}</span>
    </template>
    <template v-for="(element) in item.children" :key="element.name">
      <template v-if="element.children && element.children.length > 0">
        <el-sub-menu :index="element.name">
          <template #title>
            <el-icon>
              <component :is="element?.meta?.icon" />
            </el-icon>
            <span class="menu-title">{{ element?.meta?.title }}</span>
          </template>
          <SubMenu v-for="(subitem) in element.children" :key="subitem.name" :item="subitem"></SubMenu>
        </el-sub-menu>
      </template>
      <template v-else>
        <el-menu-item v-if="!element?.meta?.hidden" :index="element.path">
          <el-icon>
            <component :is="element?.meta?.icon" />
          </el-icon>
          <template #title>{{ element?.meta?.title }}</template>
        </el-menu-item>
      </template>

    </template>
  </el-sub-menu>
  <template v-else>
    <el-menu-item v-if="!item?.meta?.hidden" :index="item.path">
      <el-icon>
        <component :is="item?.meta?.icon" />
      </el-icon>
      <template #title>{{ item?.meta?.title }}</template>
    </el-menu-item>
  </template>
</template>
<style lang='less' scoped></style>