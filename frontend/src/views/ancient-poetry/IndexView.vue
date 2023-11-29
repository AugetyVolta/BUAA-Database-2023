
<script lang="ts" setup>
/* eslint-disable */
import { ref, reactive, } from 'vue'
import { ancientPoetryApi } from '@/apis/ancient-poetry'
import PaginationUnit from '@/components/Table/PaginationUnit.vue'
import TableUnit from '@/components/Table/TableUnit.vue';
import { useRouter, useRoute } from 'vue-router';
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
    width: 100,
  },
  {
    title: '类型',
    dataIndex: 'category',
    align: "center",
    width: 100,
  },
  {
    title: '朝代',
    dataIndex: 'dynasty',
    align: "center",
    width: 100,
  },
  {
    title: '内容',
    dataIndex: 'content',
    align: "center",
    overflow: true,
  },
  {
    title: '译文',
    dataIndex: 'translate',
    align: "center",
    overflow: true
  },
])
const categoryOption = reactive([
  '唐诗三百', '古诗三百', '宋词三百', '小学古诗', '初中古诗', '高中古诗', '宋词精选', '古诗十九', '诗经', '楚辞', '乐府', '写景', '咏物', '春天', '夏天', '秋天', '冬天',
  '写雨', '写雪', '写风', '写花', '梅花', '荷花', '菊花', '柳树', '月亮', '山水', '写山', '写水', '长江', '黄河', '儿童', '写鸟', '写马',
  '田园', '边塞', '地名', '节日', '春节', '元宵', '寒食', '清明', '端午', '七夕', '中秋', '重阳', '怀古', '抒情', '爱国', '离别', '送别', '思乡',
  '思念', '爱情', '励志', '哲理', '闺怨', '悼亡', '写人', '老师', '母亲', '友情', '战争', '读书', '惜时', '忧民', '婉约', '豪放', '民谣'
])

const dynastyOption = reactive([
  '先秦', '两汉', '魏晋', '南北朝', '隋代', '唐代', '五代', '宋代', '元代', '明代', '清代', '近现代', '金朝'
])

let list = ref([])
let total = ref<number>(0)
let isShowMoreSearch = ref<boolean>(false)
interface ParamsType {
  page: number
  limit: number
  category: string
  title: string
  dynasty: string
  author: string
  content: string
}
const query: any = route.query
let params = ref<ParamsType>({
  page: 1,
  limit: 10,
  category: '',
  title: '',
  dynasty: "",
  author: "",
  content: "",
})
if (query.limit) {
  params.value.category = query.category
  params.value.title = query.title
  params.value.dynasty = query.dynasty
  params.value.author = query.author
  params.value.content = query.content
  params.value.limit = parseInt(query.limit)
  params.value.page = parseInt(query.page)
}

const fetchTableData = () => {
  ancientPoetryApi.getAncientPoetryList(params.value).then((res: any) => {
    list.value = res.data.result
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
    category: '',
    title: '',
    dynasty: "",
    author: "",
    content: "",
  }
  fetchTableData()
}
const router = useRouter()
const linkFun = (value: any) => {
  router.push({ path: "/ancient/poetry/detail", query: { id: value.id, name: value.title, ...params.value } })
}



</script>
<template>
  <div>
    <div class="form-container">
      <div class="form-title">
        <h4>古诗学习</h4>
        <div class="button-box">
          <el-button type="primary" @click="handleSearch" icon="Search">查询</el-button>
          <el-button type="primary" @click="reSearch" plain icon="RefreshLeft">重置</el-button>
          <el-button @click="isShowMoreSearch = !isShowMoreSearch" plain
            :icon="isShowMoreSearch ? 'ArrowUp' : 'ArrowDown'">
            {{ isShowMoreSearch ? '收起' : '展开' }}
          </el-button>
        </div>
      </div>
      <div class="form-params" :style="isShowMoreSearch ? 'height:100px' : 'height:45px'">
        <el-form :inline="true" class="demo-form-inline" label-width="90px" :model="params">
          <el-form-item label="古诗标题:">
            <el-input clearable @keydown.enter="handleSearch" v-model="params.title"></el-input>
          </el-form-item>
          <el-form-item label="古诗作者:">
            <el-input clearable @keydown.enter="handleSearch" v-model="params.author"></el-input>
          </el-form-item>
          <el-form-item label="古诗内容:">
            <el-input placeholder="请输入内容关键字" clearable @keydown.enter="handleSearch" v-model="params.content"></el-input>
          </el-form-item>
          <el-form-item label="古诗类型:">
            <el-select clearable v-model="params.category">
              <el-option v-for="(item, index) in categoryOption" :label="item" :value="item"
                :key="index + 'category'"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="作者朝代:">
            <el-select clearable v-model="params.dynasty">
              <el-option v-for="(item, index) in dynastyOption" :label="item" :value="item"
                :key="index + 'dynasty'"></el-option>
            </el-select>
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

