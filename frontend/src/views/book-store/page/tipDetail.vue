


<template>
  <div>
    <el-button type="text" @click="dialog = true">发起帖子</el-button>
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
       <div class="zhihu-item-class" v-for="(item) in list">
      <el-row>
        <h3 style="float: left;margin-left: 10px" @click="intoPost(item.post_id)">{{item.post_name}}</h3>
      </el-row>
      <el-row style="margin-top: 10px;padding: 10px">
        <el-col :span="3"></el-col>
        <el-col :span="15">
        <!-- <folder >Dr.粲: 赵慧婵是我同班同学,下午热搜第二的时候班级群久违的热闹了起来。说起来我了解的我们班在清华/中科院系统中已经有三位博导了,都是30岁左右从国外被引进的,而赵慧婵无疑是其中最优秀的一位。其实我个…</folder> -->
        <el-collapse >
          <el-collapse-item title="展开">
            <div>{{item.content}}</div>
          </el-collapse-item>
        </el-collapse>
        </el-col>
      </el-row>
      <el-row style="padding: 0;margin: 0">
        <el-col :span="6">
          <el-button style="color: #0084ff;background-color: rgba(0,132,255,.1);"><i class="el-icon-caret-top"></i>赞同 {{item.supported}}</el-button>
          <el-button icon="el-icon-caret-bottom" style="color: #0084ff;background-color: rgba(0,132,255,.1);"></el-button>
        </el-col>
        <el-row>
          <el-col :span="3" style="">
            <el-button type="text" style="color: #999999;"><i class="el-icon-message"></i>{{item.commentNum}} 条评论</el-button>
          </el-col>
          <el-col :span="2" style=""> <el-button type="text" style="color: #999999;"><i class="el-icon-share"></i>分享</el-button>
          </el-col>
          <el-col :span="2" style="">
            <el-button type="text" style="color: #999999;"><i class="el-icon-star-on"></i>收藏</el-button>
          </el-col>
          <el-col :span="2" style="">
            <el-button type="text" style="color: #999999;"><i class="el-icon-heavy-rain"></i>喜欢</el-button>
          </el-col>
          <el-col :span="2">
            <el-dropdown  style="padding: 10px">
              <i class="el-icon-more"></i>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item>没有帮助</el-dropdown-item>
                <el-dropdown-item>举报</el-dropdown-item>
                <el-dropdown-item>不感兴趣</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </el-col>
          <el-col :span="3" style="">
            <el-button type="danger" icon="el-icon-delete" circle size="small" @click="userDeletePost(item.post_id)"></el-button>
          </el-col>
        </el-row>

      </el-row>
      </div>

  </div>
</template>

<script setup lang="ts">
import {ref, onMounted, reactive} from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { booksApi} from '@/apis/book-store'
import {ElMessage, FormInstance, FormRules} from "element-plus";
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

let list = ref([])



const tipData = ref({
  id: "",           //帖子id
  title: "",        //帖子名称
  author: "",       //发帖者
  content: "",      //帖子内容
  supported : 0,    //赞同数
  unsupported: 0,   //反对数
  commentNum: 0,    //评论数
  postTime: "",     //发帖时间
})
const getTip = async () => {
  const { data } = await booksApi.getTipInfo(route.query.id)
  console.log(data.data)
  list.value = data.data
}
getTip()
const posts = ref([
  {
    post_id: 1,
    post_name: 'DRX夺冠引热议,Deft最后一舞泪洒赛场',
    content: '详细略',
    post_time: '2022-11-16 21:44:30',
    comment_num: 2,
    likes_num: 999,
    create_user_name: 'ghy',
    create_user_pic: ''
  },
  {
    post_id: 2,
    post_name: '北航期末考试大作业重叠,学生不堪重负',
    content: '详细略',
    post_time: '2022-11-19 11:13:30',
    comment_num: 999,
    likes_num: 9999,
    create_user_name: '匿名',
    create_user_pic: ''
  },
]);

const getAll = () => {
  // Fetch data from API
};

const getTime = () => {
  const now = new Date();
  const yy = now.getFullYear();
  const mm = (now.getMonth() + 1).toString().padStart(2, '0');
  const dd = now.getDate().toString().padStart(2, '0');
  const hh = now.getHours().toString().padStart(2, '0');
  const mf = now.getMinutes().toString().padStart(2, '0');
  const ss = now.getSeconds().toString().padStart(2, '0');
  //gettime.value = `${yy}-${mm}-${dd} ${hh}:${mf}:${ss}`;
};

const currentTime = () => {
  setInterval(getTime, 1000);
};

const userAddTagToGroup = () => {
  //console.log(usertag.value);
  // API call to add tag to group
};

const userCreatePost = (done) => {
  //if (loading.value) {
  //  return;
  //}
  // Confirmation dialog
  //confirm('确定要提交表单吗？').then((result) => {
    //if (result) {
      //loading.value = true;
      //timer.value = setTimeout(() => {
        // Simulating API call to create a post
        //clearTimeout(timer.value);
        //loading.value = false;
        //done();
        //console.log('Post created!');
      //}, 2000);
    //}
  //});
};

const cancelForm = () => {
  //loading.value = false;
  //dialog.value = false;
  //clearTimeout(timer.value);
};

const intoPost = (id) => {
  console.log(id);
  // Navigation logic to a post page
};

const userDeletePost = (id) => {
  console.log(id);
  // API call to delete post
};

onMounted(() => {
  currentTime();
  getAll();
});
</script>

<style scoped>
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
</style>