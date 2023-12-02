<template>
  <div class="comment-section">
    <!-- 发表评论 -->
    <el-card class="comment-input">
      <el-row>
        <el-col :span="20">
          <el-input v-model="paramsForm.text" placeholder="发表评论..." clearable></el-input>
        </el-col>
        <el-col :span="4">
          <el-button type="primary" @click="postComment">发表</el-button>
        </el-col>
      </el-row>
    </el-card>

    <!-- 评论列表 -->
    <el-card v-for="comment in comments" :key="comment.id" class="comment-card">
      <div class="comment-header">
        <span>{{ comment.userName }}</span>
        <span>{{ comment.date }}</span>
      </div>
      <div class="comment-content">
        {{ comment.text }}
      </div>
      <div class="comment-footer">
        <el-button type="text" @click="deleteReply(comment.id)">删除</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import {ref, reactive} from 'vue';
import { useRouter, useRoute } from 'vue-router';
import {booksApi} from "@/apis/book-store";
import {ElMessage} from "element-plus";
import {get} from "axios";
const router = useRouter()
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

const comments = ref([])
const getComments = async () => {
  const { data } = await booksApi.getCommentInfo(route.query.id)
  console.log(data.data)
  comments.value = data.data
}
getComments()

interface paramsType {
  text: string,
  tip_id:number,
  user_id:number
}

const paramsForm = reactive<paramsType>({
   text: "",
   user_id: userData.value.id,
   tip_id:  Number(route.query.id)
})

const postComment = async () => {
  if (paramsForm.text.trim() !== '') {
    booksApi.addComment(paramsForm).then((res:any) =>{
      if (res.data.code == 200) {
        ElMessage.success("评论发表成功")
        paramsForm.text = ""
        getComments()
      }
    })
  } else {
    ElMessage.warning("评论内容不能为空")
  }
};

const deleteReply = (commentId) => {
  booksApi.deleteComment({"comment_id":commentId, "user_id":userData.value.id}).then((res:any) => {
    if (res.data.code == 200) {
      ElMessage.success("成功删除")
      getComments()
    } else {
      ElMessage.warning("你无权删除该条评论")
    }
  })
  // Handle reply functionality if needed
};
</script>

<style>
.comment-section {
  margin: 20px;
}

.comment-input {
  margin-bottom: 10px;
}

.comment-card {
  margin-bottom: 10px;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
  font-weight: bold;
}

.comment-content {
  margin-bottom: 5px;
}

.comment-footer {
  display: flex;
  justify-content: flex-end;
}
</style>