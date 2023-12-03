
<script lang="ts" setup>
/* eslint-disable */
import { ref, reactive, } from 'vue'

import { ElMessage, ElMessageBox } from 'element-plus';
import {
  taskList,
  othertaskList,
  deletetask,
  acceptPost,
  refusePost
} from '@/apis/tasks'
import PaginationUnit from '@/components/Table/PaginationUnit.vue'
import TableUnit from '@/components/Table/TableUnit.vue'
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
    title: '申请时间',
    dataIndex: 'time',
    width: 160,
    align: "center",
  },
  {
    title: '申请人',
    dataIndex: 'applier',
    align: "center",
    width: 120
  },
  {
    title: '发帖内容',
    dataIndex: 'content',
    align: "center",
    overflow: true,
    width: 160,
  },
  {
    title: '任务状态',
    dataIndex: 'status',
    align: "center",
    width: 120
  },
  {
    title: '操作',
    dataIndex: 'operate',
    align: "center",
    width: 120,
  },
])

const otherColumns = reactive([
  {
    title: '申请时间',
    dataIndex: 'time',
    width: 160,
    align: "center",
  },
  {
    title: '帖子标题',
    dataIndex: "title",
    width: 160,
    overflow: true
  },
  {
    title: "帖子内容",
    dataIndex: "content",
    width:160,
    overflow:true
  },
  {
    title: '状态',
    dataIndex: 'status',
    align: "center",
  },
])

let list = ref([])
let total = ref<number>(0)
let params = ref({
  page: 1,
  limit: 10,
  user_id: userData.value.id
})

let otherList = ref([])
let otherTotal = ref<number>(0)

let otherParams = ref({
  page:1,
  limit: 10,
  user_id: userData.value.id
})

const fetchTableData = () => {
  taskList(params.value).then((res: any) => {
    list.value = res.data.data
    total.value = res.data.total
  })
}
fetchTableData()

const otherfetchTableData = () => {
  othertaskList(params.value).then((res: any) => {
    otherList.value = res.data.data
    otherTotal.value = res.data.total
  })
}
otherfetchTableData()

const handleSizeChange = (val: number) => {
  params.value.limit = val
  params.value.page = 1
  fetchTableData()
}

const otherhandleSizeChange = (val: number) => {
  otherParams.value.limit = val
  otherParams.value.page = 1
  otherfetchTableData()
}

const handleCurrentChange = (val: number) => {
  params.value.page = val
  fetchTableData()
}

const otherhandleCurrentChange = (val: number) => {
  otherParams.value.page = val
  otherfetchTableData()
}


// const confirmEdit = () => {
//   if (taskEditForm.value.id) {
//
//     updatetask(taskEditForm.value, taskEditForm.value.id).then((res: any) => {
//       if (res.code == 200) {
//         ElMessage.success("修改成功")
//         editDialogVisible.value = false
//         fetchTableData()
//       }
//     })
//   } else {
//     addtask(taskEditForm.value).then((res: any) => {
//       if (res.code == 200) {
//         ElMessage.success("新增成功")
//         editDialogVisible.value = false
//         fetchTableData()
//       }
//     })
//   }
// }

const accept = async (value: any) => {
  acceptPost({"tip_id": value.id}).then((res:any) => {
    if (res.data.code == 200) {
       ElMessage.success("操作成功")
      fetchTableData()
      otherfetchTableData()
    } else {
      ElMessage.warning("你已完成审核")
    }
  })
}

const refuse = async (value: any) => {
  refusePost({"tip_id": value.id}).then((res:any) => {
    if (res.data.code == 200) {
       ElMessage.success("操作成功")
      fetchTableData()
      otherfetchTableData()
    } else {
      ElMessage.warning("你已完成审核")
    }
  })
}

const delRow = (value: any) => {
  ElMessageBox.confirm(
    '此操作将删除该条信息，是否继续?',
    '提示',
    {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'warning',
    }
  )
    .then(() => {
      deletetask(value.id).then((res: any) => {
        if (res.code == 200) {
          ElMessage({
            type: 'success',
            message: '删除成功',
          })
          fetchTableData()
        }
      })
    })
}


</script>
<template>
  <div class="scan-manage_layout">
    <div class="form-container">
      <div class="form-title">
        <h4>任务管理</h4>
      </div>
    </div>
    <el-row>
      <el-col span="12">
    <div class="table-box">
      <TableUnit :list="list" :columns="columns">
        <template v-slot="record">
          <el-button plain size="small" type="primary" circle @click="accept(record.record)"><el-icon style="vertical-align: middle" size="large">
      <Check/></el-icon></el-button>
          <el-button plain size="small" type="danger" circle @click="refuse(record.record)"><el-icon style="vertical-align: middle" size="large">
      <Close/></el-icon></el-button>
        </template>
      </TableUnit>
      <PaginationUnit @handleCurrentChange="handleCurrentChange" @handleSizeChange="handleSizeChange" :total="total"
        :currentPage="params.page">
      </PaginationUnit>
    </div>
      </el-col>
       <el-col span="12">
    <div class="table-box">
      <TableUnit :list="otherList" :columns="otherColumns"></TableUnit>
      <PaginationUnit @handleCurrentChange="otherhandleCurrentChange" @handleSizeChange="otherhandleSizeChange" :total="otherTotal"
        :currentPage="otherParams.page">
      </PaginationUnit>
    </div>
      </el-col>
    </el-row>
  </div>
</template>
<style lang="less" scoped></style>

