


<template>
  <div class="back">
      <el-button class="circleBtn" type="primary"
        @click="router.push({ path: '/community/communities', query: { ...route.query } })" plain icon="ArrowLeft" round>
      </el-button>
      <b>{{ quanziName }}</b>
    </div>
  <div>
    <br/>
    <el-button type="text" @click="dialog = true" style="margin-left: 5px">发起帖子</el-button>
    <el-dialog top="3%" v-model="dialog" title="创建帖子" width="50%">
        <el-form :model="newPostForm" :rules="rules" ref="ruleFormRef" class="demo-ruleForm" label-width="120px">
          <el-form-item prop="title" label="帖子标题：">
            <el-input size="large" v-model="newPostForm.title" autocomplete="off"/>
          </el-form-item>
          <el-form-item prop="content" label="帖子内容：">
            <el-input size="large" v-model="newPostForm.content" autocomplete="off"/>
          </el-form-item>
        </el-form>
          <div class="demo-drawer__footer">
            <el-button size="large" @click="dialog = false">退 出</el-button>
            <el-button size="large" type="primary" @click="onFinish(ruleFormRef)">
              提 交
            </el-button>
          </div>

      </el-dialog>

    <el-timeline class="hhh">
        <el-timeline-item v-for="(item, index) in list"  :key="index" size="large"
                          color="#0bbd87" :timestamp="item.postTime"  placement="top">
           <div class="poetry-detail-layout">
         <el-card class="box-card">
            <template #header>
               <div class="card-header">
      <el-row>
        <h3 style="float: left;margin-left: 10px">{{item.title}}</h3>
      </el-row>
                 </div>
              </template>
      <el-row style="margin-top: 10px;padding: 10px">
        <el-col :span="18">
          <div v-if="item.content.length > maxLength">
      <div v-if="!showFullContent[index]">
          {{ item.content.substring(0, maxLength) }}...
        <el-button round size="small" @click="toggleShowContent(index, true)">展开<el-icon style="vertical-align: middle">
      <ArrowDown/></el-icon></el-button>

        </div>
        <div v-else>
          {{ item.content }}
          <el-button round size="small" @click="toggleShowContent(index, false)">收起<el-icon style="vertical-align: middle">
      <ArrowUp/></el-icon></el-button>
        </div>
          </div>
          <div v-else>{{ item.content }}</div>
        </el-col>
      </el-row>
            <template #footer>
              <div>
                <div class="content">
                <el-row><p>{{item.author}}发布于{{item.exactPostTime}}</p></el-row>
                </div>
                <br/>
      <el-row style="padding: 0;margin: 0">
        <el-col :span="15">
          <el-button style="color: #0084ff;background-color: rgba(0,132,255,.1);" @click="favor(item.id)"><el-icon style="vertical-align: middle" size="large">
      <Caret-top/></el-icon>赞同 {{item.supported}}</el-button>
           <el-button style="color: #0084ff;background-color: rgba(0,132,255,.1);" @click="reject(item.id)"><el-icon style="vertical-align: middle" size="large">
      <Caret-bottom/></el-icon>反对 {{item.unsupported}}</el-button>
        </el-col>
        <el-row>
          <el-col :span="18" style="">
            <el-button type="text" style="color: #999999;" @click="intoPost(item.id)"><el-icon style="vertical-align: middle" size="large">
      <ChatRound/></el-icon>{{item.commentNum}} 条评论</el-button>
          </el-col>
          <el-col :span="6" style="">
             <el-button type="text" style="color: #999999;" @click="userDeletePost(item.id)"><el-icon style="vertical-align: middle" size="large">
      <Delete/></el-icon>删除</el-button>
          </el-col>
        </el-row>

      </el-row>
              </div>
            </template>
         </el-card>
           </div>
           </el-timeline-item>
      </el-timeline>
      </div>
</template>

<script setup lang="ts">
import {ref, onMounted, reactive, computed} from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { booksApi} from '@/apis/book-store'
import {ElMessage, ElMessageBox, FormInstance, FormRules} from "element-plus";
const router = useRouter()
const route = useRoute()
const dialog = ref(false)
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

interface newPostType {
  title: string,
  content:string,
  user_id: number,
  community_id: number
}

const newPostForm = reactive<newPostType>({
  title: "",
  content: "",
  user_id: userData.value.id,
  community_id: Number(route.query.id)
})

const rules = reactive<FormRules<typeof newPostForm>>({
  title: [
    {required: true, message: "帖子标题不能为空", trigger: "blur"}
  ],
  content: [{required: true, message: "帖子内容不能为空", trigger: "blur"}]
})

const ruleFormRef = ref()
const onFinish = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  await formEl.validate((valid, fields) => {
    if (valid) {
      booksApi.addNewPost(newPostForm).then((res: any) => {
        if (res.data.code == 200) {
          ElMessage.success("提交成功，待审核")
          dialog.value = false
        }
      })
    }
  })
}

const favor = async(id: number) => {
   booksApi.addSupport(id).then(async (res: any) => {
     if (res.data.code == 200) {
       const {data} = await booksApi.getTipInfo(route.query.id)
       console.log(data.data)
       list.value = data.data
       quanziName.value = data.title
     }
   })
}

const reject = async(id: number) => {
   booksApi.addUnsupported(id).then(async (res: any) => {
     if (res.data.code == 200) {
       const {data} = await booksApi.getTipInfo(route.query.id)
       console.log(data.data)
       list.value = data.data
       quanziName.value = data.title
     }
   })
}


const list = ref([])
const quanziName = ref("")
const maxLength = ref(20)
const showFullContent = ref([])
const toggleShowContent = (index, show) => {
  showFullContent.value[index] = show;
};
const tipData = ref({
  id: "",           //帖子id
  title: "",        //帖子名称
  author: "",       //发帖者
  content: "",      //帖子内容
  supported : 0,    //赞同数
  unsupported: 0,   //反对数
  commentNum: 0,    //评论数
  postTime: "",     //发帖时间
  exactPostTime: "", //精确发帖时间
})
const getTip = async () => {
  const { data } = await booksApi.getTipInfo(route.query.id)
  console.log(data.data)
  list.value = data.data
  quanziName.value = data.title
}
getTip()


const userAddTagToGroup = () => {
  //console.log(usertag.value);
  // API call to add tag to group
};

const intoPost = (id) => {
  router.push({ path: "/community/tip/comments", query: { id: id,} })
  // Navigation logic to a post page
};

const userDeletePost = (tip_id) => {
  console.log(tip_id)
  ElMessageBox.confirm(
    '此操作将删除该帖子，是否继续?',
    '提示',
    {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(() => {
      booksApi.deleteTipInfo({"tip_id":tip_id, "user_id":userData.value.id}).then((res: any) => {
        if (res.data.code == 200) {
          ElMessage({
            type: 'success',
            message: '删除成功',
          })
          getTip()
        } else if (res.data.code == 400) {
           ElMessage({
            type: 'error',
            message: '无权限删除该帖子',
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
  // API call to delete post
};

</script>

<style lang="less" scoped>
.pic_table {
  position: relative;
  width: 1000px;
  height: 200px;
}

.pic_table infoaddr {
  position: absolute;
  left: 120px;
  bottom: 100px;
}

.pic_table postnum {
  position: absolute;
  left: 200px;
  bottom: 100px;
}

.pic_table tagsaddr {
  position: absolute;
  left: 700px;
  bottom: 100px;
}

.pic_table tagsedit {
  position: absolute;
  left: 300px;
  bottom: 100px;
}

.pic_table tagseditcontent {
  position: absolute;
  left: 350px;
  bottom: 100px;
}

.ellipsis-text span {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: inline-block;
  max-width: 100%;
}

.box-card {
  width: 1200px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.content p {
  color: #888; /* 灰色字体颜色 */
}


.poetry-detail-layout {
  margin: 10px;
  padding: 10px;
  border-radius: 5px;

  .box-card {
    .card-header {
      line-height: 35px;
    }

    .poetry-content {
      font-weight: bold;
      line-height: 30px;
    }

    .other-data {
      text-align: center;

      dl {
        margin-top: 20px;

      }

      dd {
        padding-top: 10px;
        line-height: 30px;
        text-indent: 32px;
      }
    }
  }
}
.hhh{
  margin: 10px;
  padding: 10px;
  border-radius: 5px;
}
</style>