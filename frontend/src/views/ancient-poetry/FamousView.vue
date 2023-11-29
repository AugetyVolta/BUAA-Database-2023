
<script lang="ts" setup>
/* eslint-disable */
import { ref, } from 'vue'
import { useRouter } from 'vue-router';
import { ancientPoetryApi } from '@/apis/ancient-poetry'
const router = useRouter()
let list = ref([])
let p = 1
const fetchTableData = (page = 1) => {
  p += page
  ancientPoetryApi.getFamousList({ page, limit: 50, }).then((res: any) => {
    list.value = list.value.concat(res.data.result)
    if (p > Math.ceil(res.data.total / 50)) {
      return
    }
    fetchTableData(p)
  })
}
fetchTableData(1)

const linkFmous = (value: any) => {
  router.push({ path: "/ancient/famous/detail", query: { id: value.id, title: value.famous_name } })
}




</script>
<template>
  <div class="famous-view">
    <el-tabs type="border-card">
      <el-tab-pane label="名句集合">
        <span class="link-famous" v-for="(item, index) in list" :key="item.id">
          <el-link type="primary" @click="linkFmous(item)">{{ item.famous_name }}</el-link>
        </span>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>
<style lang="less" scoped>
.famous-view {
  padding: 20px;

  .link-famous {
    display: inline-block;
    margin: 20px;
  }
}
</style>

