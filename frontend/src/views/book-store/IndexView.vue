
<script lang="ts" setup>
/* eslint-disable */
import { ref, reactive, } from 'vue'

import { ElMessage, ElMessageBox } from 'element-plus';
import { booksApi } from '@/apis/book-store'
import PaginationUnit from '@/components/Table/PaginationUnit.vue'
import TableUnit from '@/components/Table/TableUnit.vue'
const columns = reactive([
  // {
  //   title: 'ID',
  //   dataIndex: 'id',
  //   width: 80,
  //   align: "center",
  // },
  {
    title: '书籍名称',
    dataIndex: 'name',
    align: "center",
  },
  {
    title: '书籍作者',
    dataIndex: 'author',
    align: "center",
  },
  {
    title: '作者国家',
    dataIndex: 'country',
    align: "center",
  },
  {
    title: '文学体裁',
    dataIndex: 'genre',
    align: "center",
  },
  {
    title: '添加时间',
    dataIndex: 'add_date',
    width: 160,
    align: "center",
  },
  {
    title: '创作时间(年)',
    dataIndex: 'years',
    align: "center",
  },
  {
    title: '出版社',
    dataIndex: 'publisher',
    align: "center",
  },
  {
    title: '价格(元)',
    dataIndex: 'price',
    align: "center",
    width: 100,
  },
  {
    title: '豆瓣评分',
    dataIndex: 'douban_score',
    align: "center",
    width: 100,
  },
  {
    title: '书籍简介',
    dataIndex: 'description',
    align: "center",
    overflow: true,
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
  publisher: '',
  name: '',
  startTime: '',
  endTime: '',
  author: "",
  years: "",
  genre: "",
  country: "",
})
let searchDate = ref<string[]>([params.value.startTime, params.value.endTime])

let editDialogVisible = ref(false)
interface TaskEditFormType {
  name: string
  publisher: string
  years: string
  author: string
  description: string
  price: string
  genre: string
  country: string
  id: number | null
}
let isShowMoreSearch = ref<boolean>(false)
let dataEditForm = ref<TaskEditFormType>({
  name: '',
  publisher: '',
  years: '',
  author: '',
  id: null,
  description: "",
  price: "",
  genre: "",
  country: "",
})
const fetchTableData = () => {
  booksApi.getBooksList(params.value).then((res: any) => {
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
    publisher: '',
    name: '',
    startTime: '',
    endTime: '',
    years: "",
    author: "",
    genre: "",
    country: "",
  }
  searchDate.value = []
  fetchTableData()
}

const editRow = (value: any) => {
  booksApi.getBookInfo(value.id).then((res: any) => {
    dataEditForm.value = res.data
    editDialogVisible.value = true
  })
}
const addTask = () => {
  editDialogVisible.value = true;
  dataEditForm.value = {
    name: '',
    publisher: '',
    years: '',
    author: "",
    id: null,
    description: "",
    price: "",
    genre: "",
    country: "",
  }

}
const confirmEdit = () => {
  if (!dataEditForm.value.name) {
    ElMessage.warning("书籍名不能为空")
    return
  }
  if (dataEditForm.value.id) {
    ElMessage({
      type: 'warning',
      message: '该数据禁止操作',
    })
    return
    booksApi.putBookInfo(dataEditForm.value, dataEditForm.value.id).then((res: any) => {
      if (res.code == 200) {
        ElMessage.success("修改成功")
        editDialogVisible.value = false
        fetchTableData()
      }
    })
  } else {
    booksApi.addBook(dataEditForm.value).then((res: any) => {
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
    '此操作将删除该条书籍信息，是否继续?',
    '提示',
    {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'warning',
    }
  )
    .then(() => {
      ElMessage({
        type: 'warning',
        message: '该数据禁止操作',
      })
      return
      booksApi.deleteBookInfo(value.id).then((res: any) => {
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
        <h4>书籍管理</h4>
        <div class="button-box">
          <el-button type="primary" @click="handleSearch" icon="Search">查询</el-button>
          <el-button type="primary" @click="reSearch" plain icon="RefreshLeft">重置</el-button>
          <el-button @click="addTask" plain icon="Plus">新增</el-button>
          <el-button @click="isShowMoreSearch = !isShowMoreSearch" plain
            :icon="isShowMoreSearch ? 'ArrowUp' : 'ArrowDown'">
            {{ isShowMoreSearch ? '收起' : '展开' }}
          </el-button>
        </div>
      </div>
      <div class="form-params" :style="isShowMoreSearch ? 'height:100px' : 'height:45px'">
        <el-form :inline="true" class="demo-form-inline" label-width="90px" :model="params">
          <el-form-item label="书籍名称:">
            <el-input clearable @keydown.enter="handleSearch" v-model="params.name"></el-input>
          </el-form-item>
          <el-form-item label="书籍作者:">
            <el-input clearable @keydown.enter="handleSearch" v-model="params.author"></el-input>
          </el-form-item>
          <el-form-item label="出版社:">
            <el-input clearable @keydown.enter="handleSearch" v-model="params.publisher"></el-input>
          </el-form-item>
          <el-form-item label="作者国家:">
            <el-input clearable @keydown.enter="handleSearch" v-model="params.country"></el-input>
          </el-form-item>
          <el-form-item label="文学体裁:">
            <el-input clearable @keydown.enter="handleSearch" v-model="params.genre"></el-input>
          </el-form-item>
          <el-form-item label="创作时间:">
            <el-input clearable @keydown.enter="handleSearch" v-model="params.years"></el-input>
          </el-form-item>
          <el-form-item label="添加时间:">
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
    <el-dialog title="书籍编辑" top="6vh" v-model="editDialogVisible" width="50%">
      <div>
        <el-form label-width="120px" :model="dataEditForm">
          <el-form-item label="书籍名称" required>
            <el-input v-model="dataEditForm.name"></el-input>
          </el-form-item>
          <el-form-item label="书籍作者">
            <el-input v-model="dataEditForm.author"></el-input>
          </el-form-item>
          <el-form-item label="出版社">
            <el-input v-model="dataEditForm.publisher"></el-input>
          </el-form-item>
          <el-form-item label="作者国家">
            <el-input v-model="dataEditForm.country"></el-input>
          </el-form-item>
          <el-form-item label="文学体裁">
            <el-input v-model="dataEditForm.genre"></el-input>
          </el-form-item>
          <el-form-item label="出版时间">
            <el-input v-model="dataEditForm.years"></el-input>
          </el-form-item>
          <el-form-item label="书籍定价">
            <el-input v-model="dataEditForm.price"></el-input>
          </el-form-item>
          <el-form-item label="书籍简介">
            <el-input :rows="5" type="textarea" v-model="dataEditForm.description"></el-input>
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

