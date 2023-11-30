<script lang="ts" setup>
import {ref,} from 'vue';
import {useRouter, useRoute} from 'vue-router';
import {ancientBooksApi} from '@/apis/ancient-poetry'
import {da} from "element-plus/es/locale";

const router = useRouter()
const route = useRoute()
const ancientBookData = ref({
  title: "",
  introduce: "",    //简介
  content: [],     //书评
  pic_url: "",
  label: [],      //标签
  author: ""
})
const getAncientPoetryDetail = async () => {
  const {data} = await ancientBooksApi.getAncientBooksInfo(route.query.id)
  ancientBookData.value = data.data
}
getAncientPoetryDetail()
const goIndex = () => {
  router.push({path: '/ancient/books'})
}
const scrollToElement = (index: number) => {
  const element: HTMLElement | null = document.getElementById("book" + index);
  if (element) {
    element.scrollIntoView({behavior: "smooth"});
  }
}


</script>
<template>
  <div class="book-detail-layout">
    <div class="back">
      <el-button class="circleBtn" type="primary" @click="goIndex" plain icon="ArrowLeft" round>
      </el-button>
      <b>{{ ancientBookData.title }}</b>
    </div>
    <div class="book-content scroll-bar">
      <el-backtop target=".book-content" :visibility-height="500"/>
      <el-card :body-style="{ padding: '10px' }" style="margin-bottom: 45px;">
        <div class="conent-head">
          <div class="image">
            <img :src="ancientBookData.pic_url"/>
          </div>
          <div class="bottom">
            {{ ancientBookData.introduce }}
            <div class="total-content"
                 v-if="Array.isArray(ancientBookData.content) && ancientBookData.content.length > 0">
              <h4>共有章节【{{ ancientBookData.content.length }}】章</h4>
              <span class="content-title" v-for="(item, index) in ancientBookData.content" :key="index">

                <el-link :underline="false" type="primary" @click="scrollToElement(index)">{{ item.name }}</el-link>
              </span>
            </div>
          </div>
        </div>
      </el-card>
      <el-timeline v-if="Array.isArray(ancientBookData.content)">
        <el-timeline-item v-for="(item, index) in ancientBookData.content" :id="'book' + index" size="large"
                          color="#0bbd87" :timestamp="item.name" :key="index" placement="top">
          <el-card v-if="Array.isArray(item.content_arr)">
            <p v-for="(v, i) in item.content_arr" style="padding: 10px 0;" :key="'book' + i">{{ v }}</p>
          </el-card>
        </el-timeline-item>

      </el-timeline>
    </div>
  </div>
</template>
<style lang="less" scoped>
.book-detail-layout {
  position: relative;


  .book-content {
    padding: 20px;
    height: calc(100vh - 100px);
    overflow: auto;
  }

  .conent-head {
    display: flex;

    .image {
      img {
        width: 187px;
        height: 270px;
      }
    }

    .bottom {
      padding: 20px;

      .total-content {
        padding-top: 20px;
      }

      h4 {
        padding: 5px 0;
      }

      .content-title {
        margin-right: 20px;
        line-height: 30px;
      }
    }
  }
}
</style>