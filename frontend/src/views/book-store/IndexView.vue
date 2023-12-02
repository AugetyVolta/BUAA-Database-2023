
<script lang="ts" setup>
/* eslint-disable */
import { ref, reactive, } from 'vue'

import {ElMessage, ElMessageBox, FormInstance, FormRules} from 'element-plus';
import { booksApi } from '@/apis/book-store'
import PaginationUnit from '@/components/Table/PaginationUnit.vue'
import TableUnit from '@/components/Table/TableUnit.vue'
import { useRouter, useRoute } from 'vue-router';
const route = useRoute()
const localUserData = localStorage.getItem("user_data")
interface userType {
  account: string,
  nickname: string,
  age: null | number,
  gender: string,
  id: number
}

const userForm = reactive<userType>({
  account: "",
  nickname: "",
  age: null,
  gender: "",
  id: 0
})

const userData = ref(localUserData && localUserData !== 'undefined' ? JSON.parse(localUserData as string) : userForm)
const columns = reactive([
  {
    title: '圈子名称',
    dataIndex: 'name',
    align: "center",
    isLink: true,
  },
  {
    title: '圈子简介',
    dataIndex: 'introduction',
    align: "center",
  },
  {
    title: '创建时间',
    dataIndex: 'add_date',
    width: 160,
    align: "center",
  },
  {
    title: '操作',
    dataIndex: 'operate',
    align: "center",
    width: 120,
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
  name: '',
  introduction:'',
  startTime: '',
  endTime: '',
})
let searchDate = ref<string[]>([params.value.startTime, params.value.endTime])

let editDialogVisible = ref(false)

interface TaskEditFormType {
  name: string
  introduction: string
  user_id: number
}

let dataEditForm = ref<TaskEditFormType>({
  name: "",
  introduction: "",
  user_id: userData.value.id
})
const checkQuanziName = (rule: any, value: any, callback: any) => {
  if (dataEditForm.value.name.length <= 0) {
     return callback(new Error('圈子名称不能为空'))
  }
  booksApi.checkQuanzi(dataEditForm.value.name).then((res: any) => {
    try {
      if (res.data.code == 200) {
        ElMessage.success(res.data.message)
        callback()
      } else {
        callback(new Error("圈子已存在，请重新输入"))
      }
    } catch {
      callback(new Error("圈子已存在，请重新输入"))
    }
  })
}

const rules = reactive<FormRules<typeof dataEditForm>>({
  name: [
    {required: true, validator: checkQuanziName, trigger: "blur"}
  ],
  introduction: [{required: true, message: "圈子简介不能为空", trigger: "blur"}],
})



const ruleFormRef = ref()
const fetchTableData = () => {
  booksApi.getBooksList(params.value).then((res: any) => {
    console.log(res.data.data)
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
    name: '',
    introduction:'',
    startTime: '',
    endTime: '',
  }
  searchDate.value = []
  fetchTableData()
}

const addTask = () => {
  editDialogVisible.value = true;
  dataEditForm.value = {
    name: '',
    introduction: '',
    user_id:userData.value.id
  }
}

const router = useRouter()
const linkFun = (value: any) => {
  console.log(value)
  router.push({ path: "/book-store/books/tips", query: { id: value.id, name: value.title, ...params.value } })
}


const confirmEdit = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  await formEl.validate((valid, fields) => {
    if (valid) {
       booksApi.addCommunity(dataEditForm.value).then((res: any) => {
      console.log(res.data)
      if (res.data.code == 200) {
        ElMessage.success("新增成功")
        editDialogVisible.value = false
        fetchTableData()
      }
    })
    }
  })
}

const delRow = (value: any) => {
  ElMessageBox.confirm(
    '此操作将删除该圈子，是否继续?',
    '提示',
    {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(() => {
      booksApi.deleteCommunity({"name":value.name, "user_id":dataEditForm.value.user_id}).then((res: any) => {
        if (res.data.code == 200) {
          ElMessage({
            type: 'success',
            message: '删除成功',
          })
          fetchTableData()
        } else if (res.data.code == 400) {
           ElMessage({
            type: 'error',
            message: '无权限删除该圈子',
          })
        }
      })
  })
  .catch(() => {
      ElMessage({
        type: 'info',
        message: '取消删除',
      })
    })
  return
}

</script>
<template>
  <div class="scan-manage_layout">
    <div class="form-container">
      <div class="form-title">
        <h4>圈子相关</h4>
        <div class="button-box">
          <el-button type="primary" @click="handleSearch" icon="Search">查询</el-button>
          <el-button type="primary" @click="reSearch" plain icon="RefreshLeft">重置</el-button>
          <el-button @click="addTask" plain icon="Plus">新增</el-button>
        </div>
      </div>
      <div class="form-params">
        <el-form :inline="true" class="demo-form-inline" label-width="90px" :model="params">
          <el-form-item label="圈子名称:">
            <el-input clearable @keydown.enter="handleSearch" v-model="params.name"></el-input>
          </el-form-item>
          <el-form-item label="圈子简介:">
            <el-input clearable @keydown.enter="handleSearch" v-model="params.introduction"></el-input>
          </el-form-item>
          <el-form-item label="添加时间:">
            <el-date-picker clearable v-model="searchDate" :shortcuts="pickerOptions.shortcuts"
              :disabled-date="pickerOptions.disabledDate" type="datetimerange" range-separator="至"
              value-format="YYYY-MM-DD HH:mm:ss" start-placeholder="开始日期" end-placeholder="结束日期">
            </el-date-picker>
          </el-form-item>
        </el-form>
      </div>
    </div>
    <div class="table-box">
      <TableUnit :list="list" :columns="columns" @linkFun="linkFun">
        <template v-slot="record">
          <el-button plain size="small" icon="Delete" type="danger" @click="delRow(record.record)"></el-button>
        </template>
      </TableUnit>
      <PaginationUnit @handleCurrentChange="handleCurrentChange" @handleSizeChange="handleSizeChange" :total="total"
        :currentPage="params.page">
      </PaginationUnit>
    </div>
    <el-dialog title="新建圈子" top="6vh" v-model="editDialogVisible" width="50%">
      <div>
        <el-form label-width="120px" :model="dataEditForm" :rules="rules" ref="ruleFormRef">
          <el-form-item label="圈子名称" required prop="name">
            <el-input v-model="dataEditForm.name"></el-input>
          </el-form-item>
          <el-form-item label="圈子简介" required prop="introduction">
            <el-input :rows="5" type="textarea" v-model="dataEditForm.introduction"></el-input>
          </el-form-item>
        </el-form>
      </div>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="editDialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="confirmEdit(ruleFormRef)">确 定</el-button>
        </span>
      </template>

    </el-dialog>
  </div>
</template>
<style lang="less" scoped></style>
