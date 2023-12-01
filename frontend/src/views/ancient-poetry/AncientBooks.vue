<script lang="ts" setup>
import {ref,} from 'vue'
import {useRouter, useRoute} from 'vue-router';
import {ElMessage} from 'element-plus';
import {ancientBooksApi} from '@/apis/ancient-poetry'

const router = useRouter()
const route = useRoute()

interface ParamsType {
  page: number,
  limit: number,
  name: string
}

let params = ref<ParamsType>({
  page: 1,
  limit: 10,
  name: '',
})
let list = ref([])
let total = ref(0)
let isGetMore = ref(true)
const getAncientBooksList = () => {
  //直接不循环显示
  isGetMore.value = false
  if (total.value > 0 && params.value.page * params.value.limit > 60) {
    ElMessage.success("古籍数据已全部获取完毕")
    isGetMore.value = false
    return
  }
  ancientBooksApi.getAncientBooksList(params.value).then((res: any) => {
    //res.data才是需要的数据
    list.value = list.value.concat(res.data.data)
    total.value = res.data.total
  })
}
const handleSearch = () => {
  params.value.page = 1
  list.value = []
  getAncientBooksList()
}

const loadingMoreData = () => {
  console.log("hhhhhhh " + isGetMore.value)
  if (!isGetMore.value) {
    return
  }
  getAncientBooksList()
  params.value.page += 1
}
const goBookDetail = (id: number) => {
  router.push({path: '/ancient/poetry/book', query: {id,}})
}
</script>
<template>
  <div class="ancient-books-layout">
    <div class="search-box">
      <div class="search-container">
        <h4 class="layout-title">古籍学习</h4>
        <div class="search">
          <el-input clearable @keydown.enter="handleSearch" @clear="handleSearch" size="large" v-model="params.name"
                    placeholder="请输入书籍名称">
            <template #append>
              <el-button icon="Search" @click="handleSearch"/>
            </template>
          </el-input>
        </div>
      </div>
    </div>
    <div class="content-box scroll-bar" v-infinite-scroll="loadingMoreData">
      <el-row v-if="Array.isArray(list) && list.length >0">
        <el-col v-for="(item) in list" :key="item.id" :span="6">
          <div class="content-container">
            <el-tooltip placement="right" effect="light">
              <template #content>
                <h3>
                  《{{ item.name }}》
                </h3>
                <div style="width: 350px;">
                  {{ item.description }}
                </div>
              </template>
              <img @click.stop="goBookDetail(item.id)" :src="item.pic_url" referrerPolicy="no-referrer" :alt="item.name"
                   class="image"/>
            </el-tooltip>
          </div>
        </el-col>
      </el-row>
      <div class="empty" v-else>

        <el-empty description="数据为空"/>
      </div>
    </div>
  </div>
</template>
<style lang='less' scoped>
.ancient-books-layout {
  padding: 20px;

  .search-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 20px;

    .layout-title {
      flex-grow: 1;
    }

    .search {
      flex-grow: 1.5;
    }
  }

  .search-box,
  .content-box {
    padding: 10px 0;
    margin: 10px;
    --el-table-border-color: var(--el-border-color-lighter);
    --el-table-border: 1px solid var(--el-table-border-color);
    border: var(--el-table-border);
    --el-table-bg-color: var(--el-fill-color-blank);
    background-color: var(--el-table-bg-color);
    overflow: auto;
  }
}

.content-box {
  height: calc(100vh - 185px);
  overflow-y: auto;

  .empty {
    height: calc(100vh - 250px);
    display: flex;
    align-items: center;
    justify-content: center;
  }
}

.content-container {
  text-align: center;
  padding: 10px;
}


.image {
  display: inline-block;
  width: 187px;
  height: 270px;
  cursor: pointer;
  --el-table-border-color: var(--el-border-color-lighter);
  --el-table-border: 1px solid var(--el-table-border-color);
  border: var(--el-table-border);
  margin: 20px 0;
  overflow: hidden;
  transition: all .5s;

  &:hover {
    transform: scale(1.1);
    box-shadow: 0 0 10px gray;
  }
}
</style>