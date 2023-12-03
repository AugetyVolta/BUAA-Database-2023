<script lang="ts" setup>
/* eslint-disable */
import {ref, reactive,} from 'vue'
import {ancientPoetryApi} from '@/apis/ancient-poetry'
import PaginationUnit from '@/components/Table/PaginationUnit.vue'
import TableUnit from '@/components/Table/TableUnit.vue';
import {useRouter, useRoute} from 'vue-router';
import {ElMessage, ElMessageBox, FormInstance, FormRules} from "element-plus";
import {booksApi} from "@/apis/book-store";

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

const tagOption = reactive(["古典文学", "悬疑推理", "青春文学", "科幻冒险", "心理励志", "文学经典", "历史传奇", "当代都市", "青春励志",
  "科普知识", "经济社会", "文学艺术", "人际关系", "现代都市", "科技创新", "亲情友情", "儿童成长", "文化哲学", "社会科学", "小说散文"])

let list = ref([])
let total = ref<number>(0)
let isShowMoreSearch = ref<boolean>(false)
let isLoading = ref<boolean>(false)

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
  params.value.tag = query.category
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
  router.push({path: '/library/books/book', query: {id: value.id}})
}

const digBook = () => {
  isLoading.value = true
  ancientPoetryApi.getBookFromDouBan({"user_id":userData.value.id}).then((res: any) => {
    if (res.data.code == 200) {
      ElMessage({
        type: 'success',
        message: '成功添加' + res.data.data + '本书籍',
      })
      isLoading.value = false
      fetchTableData()
    } else if (res.data.code == 400) {
      ElMessage.error("没有权限爬取书籍")
      isLoading.value = false
    }

  })
}
let editDialogVisible = ref(false)
let uploadDialogVisible = ref(false)
let changeDialogVisible = ref(false)

interface TaskEditFormType {
  name: string
  author: string
  introduction: string
  user_id: number
  tag: [],
  pic_url: string
}

let dataEditForm = ref<TaskEditFormType>({
  name: "",
  author: "",
  introduction: "",
  user_id: userData.value.id,
  tag: [],
  pic_url: ""
})

const addBook = () => {
  editDialogVisible.value = true;
  dataEditForm.value = {
    name: '',
    author: '',
    introduction: '',
    user_id: userData.value.id,
    tag: [],
    pic_url: ""
  }
}

const checkBook = (rule: any, value: any, callback: any) => {
  if (dataEditForm.value.name.length <= 0) {
    return callback(new Error('书籍标题不能为空'))
  }
  if (dataEditForm.value.author.length > 0) {
    booksApi.checkBook({name: dataEditForm.value.name, author: dataEditForm.value.author}).then((res: any) => {
      try {
        if (res.data.code == 200) {
          ElMessage.success(res.data.message)
          callback()
        } else {
          callback(new Error("书籍已存在，请重新输入"))
        }
      } catch {
        callback(new Error("书籍已存在，请重新输入"))
      }
    })
  }
}

const rules = reactive<FormRules<typeof dataEditForm>>({
  name: [
    {required: true, validator: checkBook, trigger: "blur"}
  ],
  author: [{required: true, message: "作者不能为空", trigger: "blur"}],
})

const ruleFormRef = ref()
const fileList = ref([]);
const beforeUpload = (file) => {
  // 验证上传的文件类型和大小等信息
  // 只允许上传第一张图片
  if (fileList.value.length >= 1) {
    ElMessage.error('只能上传一张图片');
    return false; // 阻止上传
  }
  fileList.value.push(file)
  return true;
};
const photoBaseUrl = 'http://10.192.187.233:9000/'
const handleUploadSuccess = (response, file, fileList) => {
  // 处理上传成功的逻辑，可以从 response 中获取上传成功后的图片地址
  dataEditForm.value.pic_url = photoBaseUrl + file.name
};
const handleUploadError = (err, file, fileList) => {
  console.log(err)
};

const handleRemove = () => {
  fileList.value.pop()
}

const confirmEdit = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  await formEl.validate((valid, fields) => {
    if (valid) {
      booksApi.addBook(dataEditForm.value).then((res: any) => {
        if (res.data.code == 200) {
          ElMessage.success("新增成功")
          editDialogVisible.value = false
          fileList.value.pop()
          fetchTableData()
        } else if (res.data.code == 400) {
          ElMessage.error("没有权限上传书籍")
          editDialogVisible.value = false
          fileList.value.pop()
        }
      })
    }
  })
}

const bookFileList = ref([]);

const uploadBook = () => {
  uploadDialogVisible.value = true;
}

const beforeUploadBook = (file) => {
  // 验证上传的文件类型和大小等信息
  const filename = file.name
  const fileExtension = filename.split('.').pop().toLowerCase();
  if (fileExtension != 'xlsx') {
    ElMessage.error('请上传xlsx文件');
    return false; // 阻止上传
  }
  // 只允许上传一份文件
  if (bookFileList.value.length >= 1) {
    ElMessage.error('只能上传一个文件');
    return false; // 阻止上传
  }
  bookFileList.value.push(file)
  return true;
};

let fileName = "";
const handleUploadBookSuccess = (response, file, fileList) => {
  // 处理上传成功的逻辑，可以从 response 中获取上传成功后的文件地址
  fileName = file.name
};

const handleBookRemove = () => {
  bookFileList.value.pop()
}

const confirmUpload = () => {
  booksApi.uploadBooks({"filename": fileName, "user_id": userData.value.id}).then((res: any) => {
    if (res.data.code == 200) {
      ElMessage.success("成功导入" + res.data.data + "本书籍")
      uploadDialogVisible.value = false
      bookFileList.value.pop()
      fetchTableData()
    } else if (res.data.code == 400) {
      ElMessage.error("没有权限上传书籍")
      uploadDialogVisible.value = false
      bookFileList.value.pop()
    }
  })
}

const delRow = (value: any) => {
  ElMessageBox.confirm(
      '此操作将删除该图书，是否继续?',
      '提示',
      {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning',
      }
  ).then(() => {
    booksApi.deleteBook({
      "title": value.title,
      "author": value.author,
      "user_id": dataEditForm.value.user_id
    }).then((res: any) => {
      if (res.data.code == 200) {
        ElMessage({
          type: 'success',
          message: '删除成功',
        })
        fetchTableData()
      } else if (res.data.code == 400) {
        ElMessage({
          type: 'error',
          message: '无权限删除该图书',
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

const downLoadBookInfo = () => {
  // 将前端数据转换为 Excel 文件
  ancientPoetryApi.downLoadBooks(userData.value.id).then((res: any) => {
    if (res.data.code == 200) {
      const fileUrl = photoBaseUrl + res.data.data
      window.open(fileUrl, '_blank');
    } else if (res.data.code == 400) {
      ElMessage.error("没有权限导出书籍")
    }
  })
}

//修改图书信息
const confirmChange = () => {
  booksApi.editBook(dataEditForm.value).then((res: any) => {
    if (res.data.code == 200) {
      ElMessage.success("修改成功")
      changeDialogVisible.value = false
      fetchTableData()
    } else if (res.data.code == 400) {
      ElMessage.error("无权限修改该图书")
      changeDialogVisible.value = false
    }
  })
}

const editRow = (value: any) => {
  changeDialogVisible.value = true
  dataEditForm.value.name = value.title
  dataEditForm.value.author = value.author
  return
}

</script>
<template>
  <div>
    <div class="form-container">
      <div class="form-title">
        <h4>翰墨阁</h4>
        <div class="button-box">
          <el-button type="primary" @click="handleSearch" icon="Search">查询</el-button>
          <el-button type="primary" @click="reSearch" plain icon="RefreshLeft">重置</el-button>
          <el-button type="primary" :disabled="isLoading" @click="digBook" plain icon="Upload">
            <span v-if="isLoading">加载中...</span>
            <span v-else>自动爬取</span>
          </el-button>
          <el-button type="primary" @click="uploadBook" plain icon="Upload">批量上传</el-button>
          <el-button type="primary" @click="downLoadBookInfo" plain icon="Download">批量导出</el-button>
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
          <el-form-item label="书籍标签:">
            <el-select clearable v-model="params.tag">
              <el-option v-for="(item, index) in tagOption" :label="item" :value="item"
                         :key="index + 'tag'"></el-option>
            </el-select>
          </el-form-item>
        </el-form>
      </div>
    </div>
    <div class="table-box">
      <TableUnit :list="list" :columns="columns" @linkFun="linkFun">
        <template v-slot="record">
          <el-button plain size="small" icon="Edit" type="primary" @click="editRow(record.record)"></el-button>
          <el-button plain size="small" icon="Delete" type="danger" @click="delRow(record.record)"></el-button>
        </template>
      </TableUnit>
      <PaginationUnit @handleCurrentChange="handleCurrentChange" @handleSizeChange="handleSizeChange" :total="total"
                      :currentPage="params.page">
      </PaginationUnit>
    </div>
    <el-dialog title="新增书籍" top="6vh" v-model="editDialogVisible" width="50%">
      <div>
        <el-form label-width="120px" :model="dataEditForm" :rules="rules" ref="ruleFormRef">
          <el-form-item label="书籍标题" required prop="name">
            <el-input v-model="dataEditForm.name"></el-input>
          </el-form-item>
          <el-form-item label="书籍作者" required prop="author">
            <el-input v-model="dataEditForm.author"></el-input>
          </el-form-item>
          <el-form-item label="书籍标签">
            <el-select clearable v-model="dataEditForm.tag" multiple>
              <el-option v-for="(item, index) in tagOption" :label="item" :value="item"
                         :key="index + 'tag'"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="书籍简介">
            <el-input :rows="5" type="textarea" v-model="dataEditForm.introduction"></el-input>
          </el-form-item>
          <el-form-item label="上传图片">
            <el-upload
                action="http://10.192.187.233:8000/api/upload"
                :before-upload="beforeUpload"
                :on-success="handleUploadSuccess"
                :on-remove="handleRemove"
                :on-error="handleUploadError"
                :file-list="fileList"
                list-type="picture-card"
                :auto-upload="true">
              <i class="el-icon-plus"></i>
            </el-upload>
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
    <el-dialog title="批量上传书籍" top="6vh" v-model="uploadDialogVisible" width="50%">
      <div>
        <el-form label-width="120px" :model="dataEditForm" :rules="rules" ref="ruleFormRef">
          <el-form-item label="上传格式">
            <el-text>(name,author,description,pic_url)</el-text>
          </el-form-item>
          <el-form-item label="上传书籍">
            <el-upload
                class="upload"
                drag
                :before-upload="beforeUploadBook"
                :on-success="handleUploadBookSuccess"
                :on-remove="handleBookRemove"
                :file-list="bookFileList"
                action="http://10.192.187.233:8000/api/upload">
              <i class="el-icon-upload"></i>
              <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
              <div class="el-upload__tip" slot="tip">只能上传.xlsx文件</div>
            </el-upload>
          </el-form-item>
        </el-form>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="uploadDialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="confirmUpload()">确 定</el-button>
        </span>
      </template>
    </el-dialog>
    <el-dialog title="编辑书籍" top="6vh" v-model="changeDialogVisible" width="50%">
      <div>
        <el-form label-width="120px" :model="dataEditForm" ref="ruleFormRef">
          <el-form-item label="书籍标签">
            <el-select clearable v-model="dataEditForm.tag" multiple>
              <el-option v-for="(item, index) in tagOption" :label="item" :value="item"
                         :key="index + 'tag'"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="书籍简介">
            <el-input :rows="5" type="textarea" v-model="dataEditForm.introduction"></el-input>
          </el-form-item>
          <el-form-item label="上传图片">
            <el-upload
                action="http://10.192.187.233:8000/api/upload"
                :before-upload="beforeUpload"
                :on-success="handleUploadSuccess"
                :on-remove="handleRemove"
                :on-error="handleUploadError"
                :file-list="fileList"
                list-type="picture-card"
                :auto-upload="true">
              <i class="el-icon-plus"></i>
            </el-upload>
          </el-form-item>
        </el-form>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="changeDialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="confirmChange()">确 定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>
<style lang="less" scoped></style>

