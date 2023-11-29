<script lang="ts" setup>
import { ref, } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { ancientPoetryApi } from '@/apis/ancient-poetry'
const router = useRouter()
const route = useRoute()
let famousList = ref([])
const fetchFamousText = (id: any) => {
  ancientPoetryApi.getFamousInfo(id).then((res: any) => {
    famousList.value = res.data
  })
}
fetchFamousText(route.query.id)


</script>
<template>
  <div class="famous-detail-layout">
    <div class="back">
      <el-button class="circleBtn" type="primary" @click="router.go(-1)" plain icon="ArrowLeft" round>
      </el-button>
      <b>{{ route.query.title }}</b>
    </div>
    <el-card class="box-card" v-for="item in famousList" :key="item.id">
      <p><b>原文：</b>{{ item.origin_text }}</p>
      <p><b>译文：</b>{{ item.translation }}</p>
    </el-card>
  </div>
</template>
<style lang="less" scoped>
.famous-detail-layout {
  .box-card {
    margin: 20px;
    line-height: 35px;
  }
}
</style>