<script lang="ts" setup>
import {onMounted, reactive, ref} from 'vue';
import {ElMessage, ElNotification} from 'element-plus';
import {useRouter} from 'vue-router';
import JSEncrypt from 'jsencrypt'
import {getVerificationCode, register, login, checkUserAccount} from '@/apis/users'
import {useMainStore} from '@/store/index'
import {useDark} from '@vueuse/core';

import type {FormInstance, FormRules} from 'element-plus'

const counterStore = useMainStore()
const isDark = useDark()
const initCanvas = () => {
  let canvas: any = document.getElementById('canvas'),
      ctx = canvas.getContext('2d'),
      w = canvas.width = window.innerWidth,
      h = canvas.height = window.innerHeight,
      hue = 217,
      stars: any = [],
      count = 0,
      maxStars = 1400;
  let canvas2: any = document.createElement('canvas')
  let ctx2: any = canvas2.getContext('2d');
  canvas2.width = 100;
  canvas2.height = 100;
  let half = canvas2.width / 2,
      gradient2 = ctx2.createRadialGradient(half, half, 0, half, half, half);
  gradient2.addColorStop(0.025, '#fff');
  gradient2.addColorStop(0.1, 'hsl(' + hue + ', 61%, 33%)');
  gradient2.addColorStop(0.25, 'hsl(' + hue + ', 64%, 6%)');
  gradient2.addColorStop(1, 'transparent');
  ctx2.fillStyle = gradient2;
  ctx2.beginPath();
  ctx2.arc(half, half, half, 0, Math.PI * 2);
  ctx2.fill();

  // End cache
  function random(min: number, max: number) {
    if (arguments.length < 2) {
      max = min;
      min = 0;
    }
    if (min > max) {
      let hold = max;
      max = min;
      min = hold;
    }
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }

  class Star {
    orbitRadius: any
    radius: any
    orbitX: any
    orbitY: any
    timePassed: any
    speed: any
    alpha: any

    constructor() {
      this.orbitRadius = random(0, w / 2 - 50);
      this.radius = random(100, this.orbitRadius) / 10;
      this.orbitX = w / 2;
      this.orbitY = h / 2;
      this.timePassed = random(0, maxStars);
      this.speed = random(0, this.orbitRadius) / 900000;
      this.alpha = random(2, 10) / 10;
      count++;
      stars[count] = this;
    }

    draw(): void {
    }
  }

  Star.prototype.draw = function () {
    let x = Math.sin(this.timePassed + 1) * this.orbitRadius + this.orbitX,
        y = Math.cos(this.timePassed) * this.orbitRadius / 2 + this.orbitY,
        twinkle = random(0, 10);
    if (twinkle === 1 && this.alpha > 0) {
      this.alpha -= 0.05;
    } else if (twinkle === 2 && this.alpha < 1) {
      this.alpha += 0.05;
    }
    ctx.globalAlpha = this.alpha;
    ctx.drawImage(canvas2, x - this.radius / 2, y - this.radius / 2, this.radius, this.radius);
    this.timePassed += this.speed;
  }
  for (let i = 0; i < maxStars; i++) {
    new Star();
  }

  function animation() {
    ctx.globalCompositeOperation = 'source-over';
    ctx.globalAlpha = 0.8;
    // ctx.fillStyle = 'hsla(' + hue + ', 64%, 6%, 1)'; 
    ctx.fillRect(0, 0, w, h)
    ctx.globalCompositeOperation = 'lighter';
    let l = stars.length;
    for (let i = 1; i < l; i++) {
      stars[i].draw();
    }
    ;
    window.requestAnimationFrame(animation);
  }

  animation();
}

const onChange = (): void => {
  counterStore.changeTheme()
}
const mainStore = useMainStore()
let isShowDialog = ref<boolean>(false)

interface userType {
  account: string,
  nickname: string,
  password: string,
  age: null | number,
  gender: string,
  profilePhoto: number
}

const userForm = reactive<userType>({
  account: "",
  nickname: "",
  password: "",
  age: null,
  gender: "",
  profilePhoto: 1
})

const checkAccount = (rule: any, value: any, callback: any) => {
  if (value.length < 5) {
    return callback(new Error('注册账号长度不得低于5位'))
  }
  checkUserAccount(userForm.account).then((res: any) => {
    try {
      if (res.data.code == 200) {
        ElMessage.success(res.data.message)
        callback()
      } else {
        callback(new Error("注册信息已存在，请重新输入"))
      }
    } catch {
      callback(new Error("注册信息已存在，请重新输入"))
    }
  })
}

const rules = reactive<FormRules<typeof userForm>>({
  account: [
    {required: true, validator: checkAccount, trigger: "blur"}
  ],
  nickname: [{required: true, message: "用户中文名不能为空", trigger: "blur"}],
  password: [{
    required: true, message: "密码不能为空", trigger: "blur"
  }],
})

const ruleFormRef = ref()
const onFinish = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  await formEl.validate((valid, fields) => {
    if (valid) {
      register(userForm).then((res: any) => {
        if (res.data.code == 200) {
          ElMessage.success("注册成功")
          isShowDialog.value = false
        }
      })
    }
  })
}

const router = useRouter()
const loginForm = reactive({
  account: "",
  password: "",
})

onMounted(() => {
  initCanvas()
})

// 获取用户代理字符串
const userLogin = () => {
  if (!loginForm.account) {
    ElMessage.warning("请输入用户名")
    return
  }
  if (!loginForm.password) {
    ElMessage.warning("请输入密码")
    return
  }
  let formData = Object.assign({}, loginForm)
  formData.password = loginForm.password
  login(formData).then((res: any) => {
    //console.log(res.code)
    console.log(res.data)
    if (res.data && res.data.code == 200) {
      localStorage.setItem("token", "success");
      //console.log(localStorage.getItem("token"))
      //console.log("login:" + res.data.data.user_data)
      localStorage.setItem("user_data", JSON.stringify(res.data.data.user_data))
      //console.log(localStorage.getItem("user_data"))
      ElMessage.success("登录成功")
      ElNotification.closeAll()
      router.push({path: "/home"})
    } else {
      ElMessage.warning("登录失败")
    }
  }).catch(() => {
    ElMessage.warning("登录失败")
  })
}
</script>
<template>
  <div class="login-layout">
    <div>
      <canvas id="canvas" v-show="isDark" :class="{ bg2: isDark }"></canvas>
      <img id="bg-img" v-show="!isDark" :class="{ bg1: !isDark }" src="@/assets/img/wallpaper.jpg" alt="">
      <el-switch class="right-switch" size="large" @change="onChange"
                 style="--el-switch-on-color: #2c2c2c; --el-switch-off-color: #f2f2f2;" v-model="isDark" inline-prompt
                 active-action-icon="Moon" inactive-action-icon="Sunny"/>
      <div class="form-layout" :style="mainStore.isDark ? '' : 'background: #fff;'">
        <h3 class="system-title">
          书缘社
          <img v-if="mainStore.isDark" src="@/assets/img/logo.png" alt="" class="logo1">
          <img v-if="!mainStore.isDark" src="@/assets/img/logo.png" alt="" class="logo">
        </h3>
        <el-form :label-position="'top'" :model="loginForm">
          <el-form-item label="登录账号：">
            <el-input prefix-icon="User" placeholder="请输入登录账号" @keydown.enter="userLogin" size="large"
                      v-model="loginForm.account"/>
          </el-form-item>
          <el-form-item label="登录密码：">
            <el-input prefix-icon="Lock" placeholder="请输入登录密码" @keydown.enter="userLogin" size="large"
                      type="password"
                      show-password v-model="loginForm.password"/>
          </el-form-item>
          <el-form-item style="padding-top: 30px;">
            <el-button size="large" style="width:66%" @click="userLogin" type="primary">登 录</el-button>
            <el-button size="large" style="width:30%" @click="isShowDialog = true" type="success" plain>注 册
            </el-button>
          </el-form-item>
        </el-form>
      </div>
      <el-dialog top="3%" v-model="isShowDialog" title="用户注册" width="50%">
        <el-form :model="userForm" :rules="rules" ref="ruleFormRef" class="demo-ruleForm" label-width="120px">
          <el-form-item prop="account" label="账号：">
            <el-input size="large" v-model="userForm.account" autocomplete="off"/>
          </el-form-item>
          <el-form-item prop="nickname" label="用户名：">
            <el-input size="large" v-model="userForm.nickname" autocomplete="off"/>
          </el-form-item>
          <el-form-item prop="password" label="密码：">
            <el-input size="large" v-model="userForm.password" autocomplete="off" show-password type="password"/>
          </el-form-item>
          <el-form-item label="年龄：" prop="age">
            <el-input size="large" type="number" v-model="userForm.age"/>
          </el-form-item>
          <el-form-item size="large" label="性别：" prop="sex">
            <el-select v-model="userForm.gender">
              <el-option label="男" value="男"></el-option>
              <el-option label="女" value="女"></el-option>
              <el-option label="保密" value="保密"></el-option>
            </el-select>
          </el-form-item>
        </el-form>

        <template #footer>
          <span class="dialog-footer">
            <el-button size="large" @click="isShowDialog = false">退 出</el-button>
            <el-button size="large" type="primary" @click="onFinish(ruleFormRef)">
              提 交
            </el-button>
          </span>
        </template>
      </el-dialog>
    </div>
  </div>
</template>

<style scoped lang="less">
.login-layout {
  position: relative;
  height: 100vh;


  .filings-number {
    width: 100vw;
    position: absolute;
    left: 0;
    text-align: center;
    bottom: 20px;
    font-size: 13px;
    color: #409eff;
  }

  @keyframes move {
    to {
      right: 5%;
    }
  }

  @keyframes bg1 {
    to {
      // transform: translateX(0%);
      opacity: 1;
    }
  }

  @keyframes bg2 {
    to {
      // transform: translateX(0%);
      opacity: 1;
    }
  }

  #bg-img {
    position: absolute;
    top: 0;
    left: 0;
    height: 100vh;
    width: 100vw;
  }

  #canvas-box {
    position: absolute;
    top: 0;
    left: 0;
    height: 100vh;
    width: 100vw;
  }

  .bg1 {
    // transform: translateX(-100%);
    opacity: .1;
    animation: bg1 3s ease-out forwards;
  }

  .bg2 {

    // transform: translateX(100%);
    opacity: .1;
    animation: bg2 3s ease-in-out forwards;
  }

  .right-switch {
    position: absolute;
    z-index: 2;
    top: 10px;
    right: 5%;
  }

  .form-layout {
    position: absolute;
    width: 400px;
    right: -30%;
    top: 0%;
    transform: translateY(60%);
    border: solid 1px #4c4d4f;
    box-shadow: inset 0 0 5px #4c4d4f;
    padding: 20px 20px 10px 20px;
    border-radius: 5px;
    animation: move 1s ease-in-out forwards;
    z-index: 9;

    .system-title {
      text-align: center;
      padding-bottom: 10px;
      position: relative;

      .logo {
        position: absolute;
        right: 10px;
        top: -10px;
        width: 66px;
        height: 66px;
      }
      .logo1 {
        position: absolute;
        right: 10px;
        top: -10px;
        width: 66px;
        height: 66px;
        filter: invert(100%);
      }
    }

    .verification-code {
      width: 45%;
      height: 40px;
      vertical-align: middle;
      margin-left: 2%;
      border-radius: 5px;
      cursor: pointer;
    }
  }
}
</style>
