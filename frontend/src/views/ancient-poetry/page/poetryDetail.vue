<script lang="ts" setup>
import { ref, } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { ancientPoetryApi } from '@/apis/ancient-poetry'
const router = useRouter()
const route = useRoute()
const ancientPoetryData = ref({
  title: "",
  category: "",
  author: "",
  dynasty: "",
  content: [],
  translate: "",
  appreciation: "",
  notes: "",
  id: null
})
const getAncientPoetryDetail = async () => {
  const { data } = await ancientPoetryApi.getAncientPoetryInfo(route.query.id)
  ancientPoetryData.value = data
}
getAncientPoetryDetail()

</script>
<template>
  <div>
    <div class="back">
      <el-button class="circleBtn" type="primary"
        @click="router.push({ path: '/ancient/poetry', query: { ...route.query } })" plain icon="ArrowLeft" round>
      </el-button>
      <b>{{ route.query.name }}</b>
    </div>
    <div class="poetry-detail-layout">

      <el-card class="box-card">
        <template #header>
          <div class="card-header">
            <h3>{{ ancientPoetryData.title }}</h3>
            <span>{{ ancientPoetryData.author }} · {{ ancientPoetryData.dynasty }} / {{ ancientPoetryData.category
            }}</span>
          </div>
        </template>
        <div class="poetry-content">
          <p v-for="(item, index) in ancientPoetryData.content" :key="index">{{ item }}</p>
          <el-divider />
        </div>
        <div class="other-data">
          <dl>
            <dt class="line blue-circle">译文</dt>
            <dd>{{ ancientPoetryData.translate }}</dd>
          </dl>
          <dl>
            <dt class="line blue-circle">注释</dt>
            <dd>{{ ancientPoetryData.notes }}</dd>
          </dl>
          <dl>
            <dt class="line blue-circle">赏析</dt>
            <dd>{{ ancientPoetryData.appreciation }}</dd>
          </dl>
        </div>
      </el-card>
    </div>
    <el-backtop />
  </div>
</template>
<style lang="less" scoped>
.poetry-detail-layout {
  margin: 10px;
  padding: 10px;
  border-radius: 5px;

  .box-card {
    text-align: center;

    .card-header {
      line-height: 35px;
    }

    .poetry-content {
      font-weight: bold;
      line-height: 30px;
    }

    .other-data {
      text-align: left;

      dl {
        margin-top: 20px;

      }

      dd {
        padding-top: 10px;
        line-height: 30px;
        text-indent: 32px;
      }
    }
  }
}
</style>