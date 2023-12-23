
<script lang="ts" setup>
import {ref, onUnmounted, onMounted} from 'vue';
import { ElLoading } from 'element-plus';
import {getAge, getRecommendedBooks, getTipsByComments, getTipsByFavor} from '@/apis/home'
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
let  tableData = ref([])
let ageData = ref([])
const getEchartsData = async () => {
  const data1 = await getRecommendedBooks()
  console.log(data1)
  dynastyCountData.value.countData = data1.data.data.bookScore
  dynastyCountData.value.category = data1.data.data.bookName
  const data2 = await getTipsByFavor()
  tableData.value = data2.data.data
  const data3 = await getAge()
  ageData.value = data3.data.data
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

const gettipsbyfavor = async () => {
  const data2 = await getTipsByFavor()
  tableData.value = data2.data.data
}

const gettipsbycomments = async () => {
  const data2 = await getTipsByComments()
  tableData.value = data2.data.data
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
    <el-carousel indicator-position="outside" height="750px" pause-on-hover="true" interval="5000">
    <el-carousel-item v-for="item in 3" :key="item">
      <div v-if="item === 1">
         <el-row class="echart-box">
      <el-col :span="24">
        <DynastyCharts v-if="dynastyCountData.category.length > 0" :countData="dynastyCountData.countData"
          :category="dynastyCountData.category"></DynastyCharts>
        <el-empty v-else description="图表数据为空" />
      </el-col>
    </el-row>
      </div>
      <div v-if="item === 2">
         <el-row class="echart-box">
      <el-col :span="24">
        <el-container style="height: 100%">
   <el-header class="header">
    <div class="header-content">
      <span class="hh">热帖榜</span>
      <div class="button-group">
        <el-button @click="gettipsbyfavor" type="primary" >按点赞数排序</el-button>
        <el-button @click="gettipsbycomments" type="success" >按评论数排序</el-button>
      </div>
    </div>
  </el-header>
    <el-main>
      <el-card >
        <el-table
    :data="tableData"
    style="width: 100%"
    height="750px"
    size="large"
  >
         <el-table-column prop="rank" label="实时排名" width="180"/>
    <el-table-column prop="date" label="发布日期"  width="180" />
    <el-table-column prop="nickname" label="发帖人" width="180" />
    <el-table-column prop="title" label="帖子标题"  />
  </el-table>
      </el-card>
    </el-main>
  </el-container>

      </el-col>
    </el-row>
      </div>
            <div v-if="item === 3">
         <el-row class="echart-box">
      <el-col :span="24">
        <PieCharts :countData="ageData"></PieCharts>
      </el-col>
    </el-row>
      </div>
    </el-carousel-item>
  </el-carousel>



  </div>
</template>


<style lang="less" scoped>
.home-layout {
  .echart-box {
    margin: 10px;
    border-radius: 5px;
    overflow: hidden;
    border: solid 1px gray;
    box-shadow: 0 0 8px gray;
    height: 88vh;
  }
}

.hh {
  font-family: Arial;
  font-weight: bold;
  font-size: 20px;
  margin-left: 10px;
  //margin-bottom: 20px;
}

.button {
  margin-top: 10px;
  margin-left: 10px;
}

.button-group {
  display: flex;
  align-items: center;
  margin-top: 3px;
  margin-right: 10px;
}

.header {
  display: flex;
  align-items: center;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 30%;
}

</style>