<script lang="ts" setup>
/* eslint-disable */
import {ref, reactive,} from 'vue'

import {ElMessage, ElMessageBox, FormInstance, FormRules} from 'element-plus';
import {booksApi, userApi} from '@/apis/book-store'
import PaginationUnit from '@/components/Table/PaginationUnit.vue'
import TableUnit from '@/components/Table/TableUnit.vue'
import {useRouter, useRoute} from 'vue-router';
import {da} from "element-plus/es/locale";

const route = useRoute()
const localUserData = localStorage.getItem("user_data")

interface userType {
  account: string,
  nickname: string,
  age: null | number,
  gender: string,
  id: number,
  privilege: number,
}

const userForm = reactive<userType>({
  account: "",
  nickname: "",
  age: null,
  gender: "",
  id: 0,
  privilege: 3,
})

const userData = ref(localUserData && localUserData !== 'undefined' ? JSON.parse(localUserData as string) : userForm)
const columns = reactive([
  {
    title: "日志id",
    dataIndex: 'logId',
    align: "center",
    width: 240
  },
  {
    title: '用户id',
    dataIndex: 'id',
    align: "center",
    // width: 160
  },
  {
    title: '用户名',
    dataIndex: 'account',
    align: "center",
    // width: 160
  },
  {
    title: '操作时间',
    dataIndex: 'time',
    align: "center",
    // width: 160
  },
  {
    title: '用户操作',
    dataIndex: 'log',
    align: "center",
    overflow: 'hidden',
  },
])


const pickerOptions = ref({
  shortcuts: [
    {
      text: '最近一周',
      value: () => {
        const end = new Date()
        const start = new Date()
        start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
        return [start, end]
      },
    },
    {
      text: '最近一个月',
      value: () => {
        const end = new Date()
        const start = new Date()
        start.setTime(start.getTime() - 3600 * 1000 * 24 * 30)
        return [start, end]
      },
    },
    {
      text: '最近三个月',
      value: () => {
        const end = new Date()
        const start = new Date()
        start.setTime(start.getTime() - 3600 * 1000 * 24 * 90)
        return [start, end]
      },
    },
  ],
  disabledDate(time: any) {
    return time.getTime() > Date.now();
  },
})

let list = ref([])
let total = ref<number>(0)
let params = ref({
  page: 1,
  limit: 10,
  log_id: '',
  id: '',
  account: '',
  operation: '',
  startTime: '',
  endTime: '',
})

let searchDate = ref<string[]>([params.value.startTime, params.value.endTime])

const fetchTableData = () => {
  userApi.getUserLogList(params.value).then((res: any) => {
    list.value = res.data.data
    total.value = res.data.total
  })
}
fetchTableData()
const handleSizeChange = (val: number) => {
  params.value.limit = val
  params.value.page = 1
  fetchTableData()
}
const handleCurrentChange = (val: number) => {
  params.value.page = val
  fetchTableData()
}
const handleSearch = () => {
  params.value.page = 1
  if (searchDate.value && searchDate.value.length > 0) {
    params.value.startTime = searchDate.value[0]
    params.value.endTime = searchDate.value[1]
  } else {
    params.value.startTime = ''
    params.value.endTime = ''
  }
  fetchTableData()
}
const reSearch = () => {
  params.value = {
    page: 1,
    limit: 10,
    log_id: '',
    id: '',
    account: '',
    operation: '',
    startTime: '',
    endTime: '',
  }
  searchDate.value = []
  fetchTableData()
}

const router = useRouter()

interface TaskEditFormType {
  user_id: number
}

let dataEditForm = ref<TaskEditFormType>({
  user_id: 0
})

const photoBaseUrl = 'http://127.0.0.1:9000/'
const downLoadLog = async () => {
  params.value.page = 1
  if (searchDate.value && searchDate.value.length > 0) {
    params.value.startTime = searchDate.value[0]
    params.value.endTime = searchDate.value[1]
  } else {
    params.value.startTime = ''
    params.value.endTime = ''
  }
  userApi.downloadUserLog(params.value).then((res: any) => {
    if (res.data.code == 200) {
      const fileUrl = photoBaseUrl + res.data.data
      window.open(fileUrl, '_blank');
    }
  })
}

//只有拥有最高权限的管理员才能进入
const privilege = userData.value.privilege
</script>
<template>
  <div v-if="privilege==1" class="scan-manage_layout">
    <div class="form-container">
      <div class="form-title">
        <h4>用户日志</h4>
        <div class="button-box">
          <el-button type="primary" @click="handleSearch" icon="Search">查询</el-button>
          <el-button type="primary" @click="reSearch" plain icon="RefreshLeft">重置</el-button>
          <el-button type="primary" @click="downLoadLog" plain icon="Download">导出日志</el-button>
        </div>
      </div>
      <div class="form-params">
        <el-form :inline="true" class="demo-form-inline" label-width="90px" :model="params">
          <el-form-item label="用户id:">
            <el-input clearable @keydown.enter="handleSearch" v-model="params.id"></el-input>
          </el-form-item>
          <el-form-item label="用户名:">
            <el-input clearable @keydown.enter="handleSearch" v-model="params.account"></el-input>
          </el-form-item>
          <el-form-item label="创建时间:">
            <el-date-picker clearable v-model="searchDate" :shortcuts="pickerOptions.shortcuts"
                            :disabled-date="pickerOptions.disabledDate" type="datetimerange" range-separator="至"
                            value-format="YYYY-MM-DD HH:mm:ss" start-placeholder="开始日期" end-placeholder="结束日期">
            </el-date-picker>
          </el-form-item>
        </el-form>
      </div>
    </div>
    <div class="table-box">
      <TableUnit :list="list" :columns="columns">
      </TableUnit>
      <PaginationUnit @handleCurrentChange="handleCurrentChange" @handleSizeChange="handleSizeChange" :total="total"
                      :currentPage="params.page">
      </PaginationUnit>
    </div>
  </div>
</template>
<style lang="less" scoped></style>
