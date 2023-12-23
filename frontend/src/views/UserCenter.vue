<!-- 
  用户中心模块：主要用于展示用户相关信息
 -->
<script lang="ts" setup>
import {ref, reactive, onMounted} from 'vue';
import {ElMessage} from 'element-plus';
import {useRouter} from 'vue-router';
import JSEncrypt from 'jsencrypt'
import {changePassword, getUserReport, modifyUserData} from '@/apis/users'
import {useMainStore} from '@/store/index'

const mainStore = useMainStore()
const router = useRouter()
const localUserData = localStorage.getItem("user_data")

interface userType {
  account: string,
  nickname: string,
  age: null | number,
  gender: string,
  privilege: number
}

const userForm = reactive<userType>({
  account: "",
  nickname: "",
  age: null,
  gender: "",
  privilege: 3
})

const userData = ref(localUserData && localUserData !== 'undefined' ? JSON.parse(localUserData as string) : userForm)
const rules = ref({
  nickname: [
    {required: true, message: '请输入姓名', trigger: 'blur'},
    {min: 2, message: '姓名长度最少为2个字符', trigger: 'blur'}
  ],
})
let showEditPssswordDialog = ref<boolean>(false)
const onSubmit = () => {
  modifyUserData(userData.value).then((res: any) => {
    //res里面有一层data,data里面有code,是两层
    if (res.data.code == 200) {
      ElMessage.success("修改成功")
      localStorage.setItem("user_data", JSON.stringify(res.data.data))
      mainStore.reloadApp()
    }
  })
}
let new_password = ''
let passwordForm = reactive({
  user_account: userData.value.account,
  old_password: "",
  new_password: "",
  confirm_new_password: "",
});
const validateRePassword = (rule: any, value: string, callback: Function) => {
  if (value != new_password) {
    callback(new Error('两次密码输入不一致'))
  } else {
    callback()
  }
}
const validatePassword = (rule: any, value: string, callback: Function) => {
  new_password = value
  if (value.length < 6) {
    callback(new Error('新密码长度不得低于6位数'))
  } else {
    callback()
  }
}
const psdEditRules = reactive({
  old_password: [{required: true, message: "请输入原始密码"}],
  new_password: [{required: true, trigger: 'change', validator: validatePassword}],
  confirm_new_password: [{required: true, trigger: 'change', validator: validateRePassword}],
})

const editPsd = () => {
  passwordForm.user_account = userData.value.account
  changePassword(passwordForm).then((res: any) => {
    console.log("wait to enter in")
    if (res.data.code === 200) {
      console.log("enter in")
      router.push({path: "/login"});
      localStorage.removeItem("token")
      localStorage.removeItem("user_data")
      ElMessage.success("密码修改成功，登录信息已注销，请重新登录");
      showEditPssswordDialog.value = false;
    }
  })
}

const photoBaseUrl = 'http://10.192.187.233:9000/'
const getReport = () => {
  getUserReport(userData.value.account).then((res: any) => {
    if (res.data.code === 200) {
      const fileUrl = photoBaseUrl + res.data.data
      window.open(fileUrl, '_blank');
    }
  })
}

onMounted(() => {
  console.log(userData.account)
  console.log("hello")
})
</script>

<template>
  <dl class="user-center-layout">
    <dt>
      <el-form :rules="rules" :model="userData" label-width="100px">
        <el-form-item label="账号：">
          <el-input size="large" v-model="userData.account" disabled></el-input>
        </el-form-item>
        <el-form-item label="姓名：" prop="user_name">
          <el-input size="large" v-model="userData.nickname"></el-input>
        </el-form-item>
        <el-form-item label="年龄：">
          <el-input size="large" v-model="userData.age" type="number"></el-input>
        </el-form-item>
        <el-form-item label="性别：" prop="sex">
          <el-select size="large" v-model="userData.gender">
            <el-option label="男" value="男"></el-option>
            <el-option label="女" value="女"></el-option>
            <el-option label="保密" value="保密"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
    </dt>
    <dd>
      <el-button icon="Top" type="primary" plain @click="$router.go(-1)">返回上级菜单</el-button>
      <el-button icon="EditPen" type="warning" plain @click="showEditPssswordDialog = true">修改登录密码</el-button>
      <el-button icon="Edit" type="primary" @click="onSubmit">修改个人信息</el-button>
      <el-button icon="Download" type="primary" @click="getReport">导出个人简报</el-button>
    </dd>
    <el-dialog title="密码修改" v-model="showEditPssswordDialog" width="50%">
      <el-form label-width="100px" :model="passwordForm" :rules="psdEditRules">
        <el-form-item prop="old_password" label="原始密码：">
          <el-input size="large" v-model="passwordForm.old_password" show-password type="password"/>
        </el-form-item>
        <el-form-item prop="new_password" label="更新密码：">
          <el-input size="large" v-model="passwordForm.new_password" show-password type="password"/>
        </el-form-item>
        <el-form-item prop="confirm_new_password" label="确认密码：">
          <el-input size="large" v-model="passwordForm.confirm_new_password" show-password type="password"/>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showEditPssswordDialog = false">取 消</el-button>
          <el-button type="primary" @click="editPsd">确 定</el-button>
        </span>
      </template>
    </el-dialog>
  </dl>
</template>
<style lang="less" scoped>
.user-center-layout {
  padding: 30px;
  position: relative;
  height: calc(100vh - 50px);

  .filings-number {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    bottom: 20px;
    font-size: 13px;
    color: #409eff;
  }
}
</style>