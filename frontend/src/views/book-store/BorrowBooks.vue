
<script lang="ts" setup>
/* eslint-disable */
import { ref, reactive, } from 'vue'

import { ElMessage, ElMessageBox } from 'element-plus';
import { borrowerApi } from '@/apis/book-store'
import PaginationUnit from '@/components/Table/PaginationUnit.vue'
import TableUnit from '@/components/Table/TableUnit.vue'
const columns = reactive([
  {
    title: '借书人',
    dataIndex: 'borrower',
    align: "center",
  },
  {
    title: '证件号',
    dataIndex: 'id_number',
    align: "center",
  },
  {
    title: '借书电话',
    dataIndex: 'phone',
    align: "center",
  },

  {
    title: '借书日期',
    dataIndex: 'borrow_date',
    width: 160,
    align: "center",
  },
  {
    title: '借书期限（天）',
    dataIndex: 'borrow_term',
    align: "center",
  },

  {
    title: '借书余额（元）',
    dataIndex: 'borrow_price',
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
  borrower: '',
  id_number: '',
  startTime: '',
  endTime: '',
})
let searchDate = ref<string[]>([params.value.startTime, params.value.endTime])

let editDialogVisible = ref(false)
interface TaskEditFormType {
  borrower: string
  phone: string
  id_number: string
  borrow_term: string
  borrow_price: string
  id: number | null
}
let dataEditForm = ref<TaskEditFormType>({
  borrower: "",
  phone: "",
  id_number: "",
  borrow_term: "",
  borrow_price: "",
  id: null
})
const fetchTableData = () => {
  borrowerApi.getBorrowerList(params.value).then((res: any) => {
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
    borrower: '',
    id_number: '',
    startTime: '',
    endTime: '',
  }
  searchDate.value = []
  fetchTableData()
}

const editRow = (value: any) => {
  borrowerApi.getBorrowerInfo(value.id).then((res: any) => {
    dataEditForm.value = res.data
    editDialogVisible.value = true
  })
}
const addTask = () => {
  editDialogVisible.value = true;
  dataEditForm.value = {
    borrower: "",
    phone: "",
    id_number: "",
    borrow_term: "",
    borrow_price: "",
    id: null
  }

}
const confirmEdit = () => {
  if (!dataEditForm.value.borrower || !dataEditForm.value.id_number) {
    ElMessage.warning("必要参数不能为空")
    return
  }
  if (dataEditForm.value.id) {
    borrowerApi.putBorrowerInfo(dataEditForm.value, dataEditForm.value.id).then((res: any) => {
      if (res.code == 200) {
        ElMessage.success("修改成功")
        editDialogVisible.value = false
        fetchTableData()
      }
    })
  } else {
    borrowerApi.addBorrower(dataEditForm.value).then((res: any) => {
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
    '此操作将删除该条借书信息，是否继续?',
    '提示',
    {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'warning',
    }
  )
    .then(() => {
      borrowerApi.deleteBorrowerInfo(value.id).then((res: any) => {
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
        <h4>借书管理</h4>
        <div class="button-box">
          <el-button type="primary" @click="handleSearch" icon="Search">查询</el-button>
          <el-button type="primary" @click="reSearch" plain icon="RefreshLeft">重置</el-button>
          <el-button @click="addTask" plain icon="Plus">新增</el-button>
        </div>
      </div>
      <div class="form-params">
        <el-form :inline="true" class="demo-form-inline" label-width="90px" :model="params">
          <el-form-item label="借书人:">
            <el-input clearable @keydown.enter="handleSearch" placeholder="请输入借书人姓名" v-model="params.borrower"></el-input>
          </el-form-item>
          <el-form-item label="证件号:">
            <el-input clearable @keydown.enter="handleSearch" placeholder="请输入借书人完整证件号"
              v-model="params.id_number"></el-input>
          </el-form-item>
          <el-form-item label="借书日期:">
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
    <el-dialog title="借书信息编辑" v-model="editDialogVisible" width="50%">
      <div>
        <el-form label-width="120px" :model="dataEditForm">
          <el-form-item label="借书人" required>
            <el-input v-model="dataEditForm.borrower"></el-input>
          </el-form-item>
          <el-form-item label="证件号" required>
            <el-input v-model="dataEditForm.id_number"></el-input>
          </el-form-item>
          <el-form-item label="借书电话">
            <el-input v-model="dataEditForm.phone"></el-input>
          </el-form-item>
          <el-form-item label="借书期限（天）">
            <el-input v-model="dataEditForm.borrow_term"></el-input>
          </el-form-item>
          <el-form-item label="借书余额（元）">
            <el-input v-model="dataEditForm.borrow_price"></el-input>
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

