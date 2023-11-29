
<script lang="ts" setup>
/* eslint-disable */
import { ref, reactive, } from 'vue'

import { ElMessage, ElMessageBox } from 'element-plus';
import {
  taskList,
  addtask,
  updatetask,
  deletetask,
  taskdetail,
} from '@/apis/tasks'
import PaginationUnit from '@/components/Table/PaginationUnit.vue'
import TableUnit from '@/components/Table/TableUnit.vue'
const columns = reactive([
  {
    title: 'ID',
    dataIndex: 'id',
    width: 80,
    align: "center",
  },
  {
    title: '任务名称',
    dataIndex: 'name',
    align: "center",
    overflow: true,
  },
  {
    title: '任务时间',
    dataIndex: 'time',
    width: 160,
    align: "center",
  },
  {
    title: '任务状态',
    dataIndex: 'status',
    align: "center",
  },
  {
    title: '申请人',
    dataIndex: 'reporter',
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
  reporter: '',
  name: '',
  startTime: '',
  endTime: '',
  status: "",
})
let searchDate = ref<string[]>([params.value.startTime, params.value.endTime])

let editDialogVisible = ref(false)
interface TaskEditFormType {
  name: string
  reporter: string
  status: string
  id: number | null
}
let taskEditForm = ref<TaskEditFormType>({
  name: '',
  reporter: '',
  status: '',
  id: null,
})
const fetchTableData = () => {
  taskList(params.value).then((res: any) => {
    list.value = res.data.result
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
    reporter: '',
    name: '',
    startTime: '',
    endTime: '',
    status: "",
  }
  searchDate.value = []
  fetchTableData()
}

const editRow = (value: any) => {
  taskdetail(value.id).then((res: any) => {
    taskEditForm.value = res.data
    editDialogVisible.value = true
  })
}
const addTask = () => {
  editDialogVisible.value = true;
  taskEditForm.value = {
    name: '',
    reporter: '',
    status: '',
    id: null,
  }

}
const confirmEdit = () => {
  if (taskEditForm.value.id) {

    updatetask(taskEditForm.value, taskEditForm.value.id).then((res: any) => {
      if (res.code == 200) {
        ElMessage.success("修改成功")
        editDialogVisible.value = false
        fetchTableData()
      }
    })
  } else {
    addtask(taskEditForm.value).then((res: any) => {
      if (res.code == 200) {
        ElMessage.success("新增成功")
        editDialogVisible.value = false
        fetchTableData()
      }
    })
  }
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
        <div class="button-box">
          <el-button type="primary" @click="handleSearch" icon="Search">查询</el-button>
          <el-button type="primary" @click="reSearch" plain icon="RefreshLeft">重置</el-button>
          <el-button @click="addTask" plain icon="Plus">新建</el-button>
        </div>
      </div>
      <div class="form-params">
        <el-form :inline="true" class="demo-form-inline" label-width="100px" :model="params">
          <el-form-item label="任务名称:">
            <el-input clearable @keydown.enter="handleSearch" v-model="params.name" placeholder="请输入任务名称"></el-input>
          </el-form-item>
          <el-form-item label="申请人:">
            <el-input clearable @keydown.enter="handleSearch" v-model="params.reporter" placeholder="请输入申请人名称"></el-input>
          </el-form-item>
          <el-form-item label="结束日期:">
            <el-date-picker clearable v-model="searchDate" :shortcuts="pickerOptions.shortcuts"
              :disabled-date="pickerOptions.disabledDate" type="datetimerange" range-separator="至"
              value-format="YYYY-MM-DD hh:mm:ss" start-placeholder="开始日期" end-placeholder="结束日期">
            </el-date-picker>
          </el-form-item>
        </el-form>
      </div>
    </div>
    <div class="table-box">
      <TableUnit :list="list" :columns="columns">
        <template v-slot="record">
          <el-button plain size="small" icon="Edit" type="primary" @click="editRow(record.record)"></el-button>
          <el-button plain size="small" icon="Delete" type="danger" @click="delRow(record.record)"></el-button>
        </template>
      </TableUnit>
      <PaginationUnit @handleCurrentChange="handleCurrentChange" @handleSizeChange="handleSizeChange" :total="total"
        :currentPage="params.page">
      </PaginationUnit>
    </div>
    <el-dialog title="任务编辑" v-model="editDialogVisible" width="50%">
      <div>
        <el-form label-width="120px" :model="taskEditForm">
          <el-form-item label="任务名称">
            <el-input v-model="taskEditForm.name"></el-input>
          </el-form-item>
          <el-form-item label="申请人">
            <el-input v-model="taskEditForm.reporter"></el-input>
          </el-form-item>
          <el-form-item label="任务状态">
            <el-input v-model="taskEditForm.status"></el-input>
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

