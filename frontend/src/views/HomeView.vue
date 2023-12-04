
<script lang="ts" setup>
import {ref, onUnmounted, onMounted} from 'vue';
import { ElLoading } from 'element-plus';
import { getPoetryCountTotal, getRecommendedBooks } from '@/apis/home'
import AuthorCharts from '@/components/Echarts/AuthorCharts.vue';
import PieCharts from '@/components/Echarts/PieCharts.vue';
import DynastyCharts from '@/components/Echarts/DynastyCharts.vue';
let dynastyCountData = ref({
  countData: [],
  category: [],
})
let authorCountData = ref({
  countData: [],
  category: [],
})
let authorByDynastyCountData = ref({
  countData: [],
  category: [],
})
const getEchartsData = async () => {
  const data1 = await getRecommendedBooks()
  console.log(data1)
  dynastyCountData.value.countData = data1.data.data.bookScore
  dynastyCountData.value.category = data1.data.data.bookName
  // const { data } = await getPoetryCountTotal()
  // data.dynasty_poems.forEach((element: any) => {
  //   dynastyCountData.value.countData.push(element.poem_count)
  //   dynastyCountData.value.category.push(element.dynasty)
  // });
  // data.author_poems.forEach((element: any) => {
  //   authorCountData.value.countData.push({ name: element.author, value: element.poem_count })
  //   authorCountData.value.category.push(element.author)
  // });
  // data.poet_count_author_by_dynasty.forEach((element: any) => {
  //   authorByDynastyCountData.value.category.push(element.dynasty)
  //   authorByDynastyCountData.value.countData.push(element.author_count)
  // });
}
let timer: null | any = null
let previousHeight: number = 0
let isReload = ref(true)
let loadingInstance: any = null
const onResize = () => {
  var currentHeight = window.innerHeight;
  if (timer || currentHeight === previousHeight) return
  timer = setTimeout(() => {
    isReload.value = false
    loadingInstance = ElLoading.service({
      lock: true,
      text: '系统视图切换中，请稍候...',
      background: 'rgba(0, 0, 0, 0.5)',
    })
    let fullScreenTimer: null | any = null
    fullScreenTimer = setTimeout(() => {
      previousHeight = currentHeight
      isReload.value = true
      if (loadingInstance) {
        loadingInstance.close()
      }
      if (fullScreenTimer) {
        clearTimeout(fullScreenTimer)
      }
    }, 1000);
    if (timer) {
      clearTimeout(timer);
      timer = null;
    }
  }, 500);
}

window.addEventListener("resize", onResize);
onUnmounted(() => {
  window.removeEventListener("resize", onResize)
})
onMounted(() => {
  console.log("homeView")
})
getEchartsData()
</script>
<template>
  <div class="home-layout" v-if="isReload">
    <el-row class="echart-box">
      <el-col :span="24">
        <DynastyCharts v-if="dynastyCountData.category.length > 0" :countData="dynastyCountData.countData"
          :category="dynastyCountData.category"></DynastyCharts>
        <el-empty v-else description="图表数据为空" />
      </el-col>
    </el-row>
    <el-row class="echart-box">
      <el-col :span="24">
        <AuthorCharts v-if="authorByDynastyCountData.category.length > 0" :category="authorByDynastyCountData.category"
          :countData="authorByDynastyCountData.countData"></AuthorCharts>
        <el-empty v-else description="图表数据为空" />
      </el-col>
    </el-row>
    <el-row class="echart-box scroll-bar" style="overflow-y: auto;">
      <el-col :span="24">
        <PieCharts v-if="authorCountData.category.length > 0" :countData="authorCountData.countData"
          :category="authorCountData.category"></PieCharts>
        <el-empty v-else description="图表数据为空" />
      </el-col>
    </el-row>

  </div>
</template>
<style lang="less" scoped>
.home-layout {
  .echart-box {
    margin: 20px;
    border-radius: 5px;
    overflow: hidden;
    border: solid 1px gray;
    box-shadow: 0 0 8px gray;
    height: 88vh;
  }
}
</style>