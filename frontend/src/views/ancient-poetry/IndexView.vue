<script lang="ts" setup>
/* eslint-disable */
import {ref, reactive,} from 'vue'
import {ancientPoetryApi} from '@/apis/ancient-poetry'
import PaginationUnit from '@/components/Table/PaginationUnit.vue'
import TableUnit from '@/components/Table/TableUnit.vue';
import {useRouter, useRoute} from 'vue-router';

const route = useRoute()
const columns = reactive([
  {
    title: '标题',
    dataIndex: 'title',
    align: "center",
    isLink: true,
  },
  {
    title: '作者',
    dataIndex: 'author',
    align: "center",
    width: 200,
  },
  {
    title: '简介',
    dataIndex: 'introduction',
    align: "center",
    overflow: true,
  },
  {
    title: '标签',
    dataIndex: 'tag',
    align: "center",
    width: 300,
  },
  {
    title: '评分',
    dataIndex: 'score',
    align: "center",
    width: 200,
  },
  {
    title: '收藏数',
    dataIndex: 'liked_times',
    align: "center",
    width: 200,
  },
  {
    title: '操作',
    dataIndex: 'operate',
    align: "center",
    width: 120,
  },
])


let list = ref([])
let total = ref<number>(0)
let isShowMoreSearch = ref<boolean>(false)

interface ParamsType {
  page: number
  limit: number
  id: number
  title: string
  author: string
  introduction: string
  tag: string
  score: number
  liked_times: number
}

const query: any = route.query
let params = ref<ParamsType>({
  page: 1,
  limit: 10,
  id: 0,
  title: "",
  author: "",
  introduction: "",
  tag: "",
  score: 0.0,
  liked_times: 0,
})
if (query.limit) {
  params.value.title = query.title
  params.value.author = query.author
  params.value.introduction = query.introduction
  params.value.limit = parseInt(query.limit)
  params.value.page = parseInt(query.page)
}

const fetchTableData = () => {
  ancientPoetryApi.getAncientPoetryList(params.value).then((res: any) => {
    list.value = res.data.data
    total.value = res.data.total
  })
}
fetchTableData()
const handleSearch = () => {
  params.value.page = 1
  fetchTableData()
}
const handleSizeChange = (val: number) => {
  params.value.limit = val
  params.value.page = 1
  fetchTableData()
}
const handleCurrentChange = (val: number) => {
  params.value.page = val
  fetchTableData()
}
const reSearch = () => {
  params.value = {
    page: 1,
    limit: 10,
    id: 0,
    title: "",
    author: "",
    introduction: "",
    tag: "",
    score: 0.0,
    liked_times: 0,
  }
  fetchTableData()
}
const router = useRouter()
const linkFun = (value: any) => {
  router.push({path: '/ancient/poetry/book', query: {id: value.id}})
}

const addBook = () => {

}

</script>
<template>
  <div>
    <div class="form-container">
      <div class="form-title">
        <h4>书籍管理</h4>
        <div class="button-box">
          <el-button type="primary" @click="handleSearch" icon="Search">查询</el-button>
          <el-button type="primary" @click="reSearch" plain icon="RefreshLeft">重置</el-button>
          <el-button @click="addBook" plain icon="Plus">新增</el-button>
        </div>
      </div>
      <div class="form-params" :style="isShowMoreSearch ? 'height:100px' : 'height:45px'">
        <el-form :inline="true" class="demo-form-inline" label-width="90px" :model="params">
          <el-form-item label="书籍标题:">
            <el-input clearable @keydown.enter="handleSearch" v-model="params.title"></el-input>
          </el-form-item>
          <el-form-item label="书籍作者:">
            <el-input clearable @keydown.enter="handleSearch" v-model="params.author"></el-input>
          </el-form-item>
          <el-form-item label="书籍内容:">
            <el-input placeholder="请输入内容关键字" clearable @keydown.enter="handleSearch"
                      v-model="params.introduction"></el-input>
          </el-form-item>
        </el-form>
      </div>
    </div>
    <div class="table-box">
      <TableUnit :list="list" @linkFun="linkFun" :columns="columns">
      </TableUnit>
      <PaginationUnit @handleCurrentChange="handleCurrentChange" @handleSizeChange="handleSizeChange" :total="total"
                      :currentPage="params.page">
      </PaginationUnit>
    </div>

  </div>
</template>
<style lang="less" scoped></style>

