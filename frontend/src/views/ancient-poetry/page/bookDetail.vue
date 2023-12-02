<script lang="ts" setup>
import {reactive, ref,} from 'vue';
import {useRouter, useRoute} from 'vue-router';
import {ancientBooksApi} from '@/apis/ancient-poetry'
import {da} from "element-plus/es/locale";
import {ElMessage, FormInstance} from "element-plus";
import {register} from "@/apis/users";

const router = useRouter()
const route = useRoute()
const localUserData = localStorage.getItem("user_data")

const ancientBookData = ref({
  title: "",
  introduce: "",    //简介
  content: [],     //书评
  pic_url: "",
  label: [],      //标签
  author: "",
  average_score: 0.0,
  isBookFavorite: false, // 添加这个属性来表示书籍是否已经收藏
})

// const scrollToElement = (index: number) => {
//   const element: HTMLElement | null = document.getElementById("book" + index);
//   if (element) {
//     element.scrollIntoView({behavior: "smooth"});
//   }
// }

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

const getAncientPoetryDetail = async () => {
  const {data} = await ancientBooksApi.getAncientBooksInfo({"id": route.query.id, "user_id": userData.value.id})
  ancientBookData.value = data.data
}
getAncientPoetryDetail()
const goIndex = () => {
  router.push({path: '/ancient/books'})
}

const newReviewFormRef = ref(null);
let addReviewDialogVisible = ref<boolean>(false);

interface reviewFrom {
  reviewContent: string,
  starRating: number,
  user_id: number,
  book_id: number,
}

const newReview = reactive<reviewFrom>({
  reviewContent: '',
  starRating: 0,
  user_id: userData.value.id,
  book_id: Number(route.query.id),
})

const newReviewFormRules = {
  reviewContent: [
    {required: true, message: '请输入书评内容', trigger: 'blur'}
  ]
};

const submitReview = async () => {
  if (newReview.reviewContent == "") {
    ElMessage.warning("书评内容不可为空")
    resetForm()
  } else {
    ancientBooksApi.addNewReview(newReview).then(async (res: any) => {
      if (res.data.code == 200) {
        ElMessage.success("书评添加成功")
        const {data} = await ancientBooksApi.getAncientBooksInfo({id: route.query.id, user_id: userData.value.id})
        ancientBookData.value = data.data
        addReviewDialogVisible.value = false;
      }
    })
  }
}

function resetForm() {
  newReview.reviewContent = '';
  newReview.starRating = 0;
}

//收藏

interface favouriteFrom {
  user_id: number,
  book_id: number,
}

const favourite = reactive<favouriteFrom>({
  user_id: userData.value.id,
  book_id: Number(route.query.id),
})

//实现收藏逻辑
const addToFavorites = () => {
  ancientBooksApi.addToFavorites(favourite).then(async (res: any) => {
    if (res.data.code == 200) {
      ElMessage.success("收藏成功")
    }
  })
  ancientBookData.value.isBookFavorite = true;
};

//取消收藏
const removeFromFavorites = () => {
  ancientBooksApi.removeFromFavorites(favourite).then(async (res: any) => {
    if (res.data.code == 200) {
      ElMessage.success("取消收藏成功")
    }
  })
  ancientBookData.value.isBookFavorite = false;
};

</script>
<template>
  <div class="book-detail-layout">
    <div class="back">
      <el-button class="circleBtn" type="primary" @click="goIndex" plain icon="ArrowLeft" round>
      </el-button>
      <b>{{ ancientBookData.title }}</b>
    </div>
    <div class="book-content scroll-bar">
      <el-backtop target=".book-content" :visibility-height="500"/>
      <el-card :body-style="{ padding: '10px' }" style="margin-bottom: 45px;">
        <div class="conent-head">
          <div class="image">
            <img :src="ancientBookData.pic_url" referrerPolicy="no-referrer"/>
          </div>
          <div class="bottom">
            <p class="author">{{ "作者：" + ancientBookData.author }}</p>
            <p class="introduction">{{ "简介：" + ancientBookData.introduce }}</p>
            <div class="labels">
              #标签：
              <span class="label" v-for="(item, index) in ancientBookData.label" :key="index">
            {{ item }}
          </span>
            </div>
            <div class="rating">
              <el-rate v-model="ancientBookData.average_score" size="large" show-score="true" allow-half disabled
                       score-template="{value} 分"></el-rate>
            </div>
            <!-- 添加红心按钮 -->
            <el-button type="danger" v-if="!ancientBookData.isBookFavorite" @click="addToFavorites">
              <i class="el-icon-heart-off"></i> 收藏
            </el-button>
            <el-button type="danger" v-else @click="removeFromFavorites">
              <i class="el-icon-heart-on"></i> 取消收藏
            </el-button>
          </div>
        </div>
      </el-card>
      <el-button type="primary" @click="addReviewDialogVisible = true">增加书评</el-button>
      <el-dialog title="增加书评" v-model="addReviewDialogVisible" width="40%">
        <el-form :model="newReview" :rules="newReviewFormRules" ref="newReviewFormRef">
          <el-form-item label="书评内容" prop="reviewContent">
            <el-input v-model="newReview.reviewContent" type="textarea" :rows="4"></el-input>
          </el-form-item>
          <el-form-item label="五星评价">
            <el-rate v-model="newReview.starRating" :max="5" allow-half show-score></el-rate>
          </el-form-item>
          <el-form-item>
            <div class="button-group">
              <el-button type="primary" @click="submitReview">提交</el-button>
              <el-button @click="resetForm">重置</el-button>
            </div>
          </el-form-item>
        </el-form>
      </el-dialog>
      <br/>
      <br>
      <el-timeline v-if="Array.isArray(ancientBookData.content)">
        <el-timeline-item v-for="(item, index) in ancientBookData.content" :id="'book' + index" size="large"
                          color="#0bbd87" :timestamp="item.name" :key="index" placement="top">
          <el-card v-if="Array.isArray(item.content_arr)">
            <el-rate v-model="item.score" :max="5" :show-text="false" :disabled="true"></el-rate>
            <p v-for="(v, i) in item.content_arr" style="padding: 10px 0;" :key="'book' + i">{{ v }}</p>
            <p style="margin-top: 10px;color: #888888;">{{ new Date(item.create_time).toLocaleString() }}</p>
          </el-card>
        </el-timeline-item>
      </el-timeline>
    </div>
  </div>
</template>
<style lang="less" scoped>
.button-group {
  display: flex;
  justify-content: center;
  width: 100%;
  margin-top: 20px;
}

.button-group > .el-button + .el-button {
  margin-left: 30px;
}

.add-review-btn {
  float: right;
}

.rating {
  display: flex;
  align-items: center;
  margin-top: 15px;
}

.rating-value {
  margin-left: 10px;
  font-size: 16px;
  font-weight: bold;
}

.label {
  margin-right: 8px;
  margin-bottom: 8px;
  color: #409eff;
}

.author {
  margin-bottom: 8px;
  font-weight: bold;
}

.labels {
  margin-top: auto;
  padding-top: 10px;
  border-top: 1px solid #ebeef5;
  display: flex;
  flex-wrap: wrap;
}

.introduction {
  margin-bottom: 16px;
}


.book-detail-layout {
  position: relative;


  .book-content {
    padding: 20px;
    height: calc(100vh - 100px);
    overflow: auto;
  }

  .conent-head {
    display: flex;

    .image {
      img {
        width: 187px;
        height: 270px;
      }
    }

    .bottom {
      padding: 20px;

      .total-content {
        padding-top: 20px;
      }

      h4 {
        padding: 5px 0;
      }

      .content-title {
        margin-right: 20px;
        line-height: 30px;
      }
    }
  }
}
</style>