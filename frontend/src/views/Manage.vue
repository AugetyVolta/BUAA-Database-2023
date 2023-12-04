<script lang="ts" setup>
/* eslint-disable */
import {ref, reactive,} from 'vue'

import {ElMessage, ElMessageBox, FormInstance, FormRules} from 'element-plus';
import {booksApi, userApi} from '@/apis/book-store'
import PaginationUnit from '@/components/Table/PaginationUnit.vue'
import TableUnit from '@/components/Table/TableUnit.vue'
import {useRouter, useRoute} from 'vue-router';

const route = useRoute()
const localUserData = localStorage.getItem("user_data")

interface userType {
  account: string,
  nickname: string,
  age: null | number,
  gender: string,
  id: number,
  privilege: number
}

const userForm = reactive<userType>({
  account: "",
  nickname: "",
  age: null,
  gender: "",
  id: 0,
  privilege: 3
})

const userData = ref(localUserData && localUserData !== 'undefined' ? JSON.parse(localUserData as string) : userForm)
const columns = reactive([
  {
    title: '用户id',
    dataIndex: 'id',
    align: "center",
  },
  {
    title: '用户名',
    dataIndex: 'account',
    align: "center",
  },
  {
    title: '用户昵称',
    dataIndex: 'nickname',
    align: "center",
  },
  {
    title: '权限',
    dataIndex: 'privilege',
    align: "center",
    width: 120,
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
let params = ref({
  page: 1,
  limit: 10,
  id: '',
  account: '',
  nickname: '',
  privilege: 3
})

interface TaskEditFormType {
  user_id: number
  privilege: number
}

let dataEditForm = ref<TaskEditFormType>({
  user_id: 0,
  privilege: 0
})

const fetchTableData = () => {
  userApi.getUserList(params.value).then((res: any) => {
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
  fetchTableData()
}
const reSearch = () => {
  params.value = {
    page: 1,
    limit: 10,
    id: '',
    account: '',
    nickname: '',
    privilege: 3
  }
  fetchTableData()
}

const router = useRouter()
let editDialogVisible = ref(false)
const editRow = (value: any) => {
  editDialogVisible.value = true
  dataEditForm.value.user_id = value.id
  dataEditForm.value.privilege = value.privilege
  return
}

const confirmEdit = async () => {
  userApi.modify_userPrivilege(dataEditForm.value).then((res: any) => {
    if (res.data.code == 200) {
      ElMessage.success("修改成功")
      editDialogVisible.value = false
      fetchTableData()
    }
  })
}

</script>
<template>
  <div class="scan-manage_layout">
    <div class="form-container">
      <div class="form-title">
        <h4>用户管理</h4>
        <div class="button-box">
          <el-button type="primary" @click="handleSearch" icon="Search">查询</el-button>
          <el-button type="primary" @click="reSearch" plain icon="RefreshLeft">重置</el-button>
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
          <el-form-item label="用户昵称:">
            <el-input clearable @keydown.enter="handleSearch" v-model="params.nickname"></el-input>
          </el-form-item>
        </el-form>
      </div>
    </div>
    <div class="table-box">
      <TableUnit :list="list" :columns="columns">
        <template v-slot="record">
          <el-button plain size="small" icon="Edit" type="primary" @click="editRow(record.record)"></el-button>
        </template>
      </TableUnit>
      <PaginationUnit @handleCurrentChange="handleCurrentChange" @handleSizeChange="handleSizeChange" :total="total"
                      :currentPage="params.page">
      </PaginationUnit>
    </div>
    <el-dialog title="修改权限" top="6vh" v-model="editDialogVisible" width="50%">
      <div>
        <el-form label-width="120px" :model="dataEditForm">
          <el-form-item label="用户权限">
            <el-input size="large" type="number" v-model="dataEditForm.privilege" :min="1" :max="3"/>
          </el-form-item>
        </el-form>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="editDialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="confirmEdit">确 定</el-button>
        </span>
      </template>

    </el-dialog>
  </div>
</template>
<style lang="less" scoped></style>
