import axios from 'axios'
import { AxiosRequestConfig, AxiosError, AxiosResponse, InternalAxiosRequestConfig } from 'axios'
import { ElMessage, ElLoading, ElNotification } from 'element-plus'
import { start, close } from './nporgress'
import router from '@/router/index'
/* eslint-disable */
// const baseURL = 'http://127.0.0.1:9000' //本地测试环境
//const baseURL = 'http://127.0.0.1:8000/' //服务器地址
const baseURL = 'http://10.192.187.233:8000/'
axios.defaults.withCredentials = true
const service = axios.create({
  baseURL,
  timeout: 5000,
    headers:{
    "Content-type":"application/json;charset:utf-8"
    }
})
let loadingInstance: any = undefined;
service.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    if (config && config.headers) {
      start()
      loadingInstance = ElLoading.service({
        lock: true,
        text: '加载中，请稍候...',
        background: 'rgba(0, 0, 0, 0.5)',
      })
      if (localStorage.getItem("token") && localStorage.getItem("token") !== 'undefined') {
        config.headers['token'] = localStorage.getItem("token")
      }
    }
    return config;
  },
  error => {
    return Promise.reject(error)
  }
)

service.interceptors.response.use(
  (response: any) => {
    const res = response.data
    close();
    if (loadingInstance) {
      loadingInstance.close()
    }
    switch (res.code) {
      case 200:
        return res
      case 401:
        localStorage.setItem("token", res.data)
        return service(response.config)
        break;
      case 403:
        ElNotification({
          message: res.message,
          type: 'error',
          duration: 0
        })
        router.push({ path: "/login" })
        break
      default:
        ElNotification({
          message: res.message || '请求错误',
          type: 'error',
          duration: 5 * 1000
        })
        break;
    }
  },
  async (error: AxiosError) => {
    close();
    if (loadingInstance) {
      loadingInstance.close()
    }
    if (error.message.includes("timeout")) {
      ElNotification.error("请求超时，请稍后再试");
    } else {
      ElNotification({
        message: error.message || '服务器请求错误，请稍后重试',
        type: 'error',
        duration: 5 * 1000
      })

    }
    return Promise.reject(error);
  }
)

// 文件下载通用方式

export const requestFile = axios.create({
  baseURL,
  timeout: 0, //关闭超时时间
});

requestFile.interceptors.request.use((config) => {
  config.headers['token'] = localStorage.getItem("token") //携带的请求头
  config.responseType = 'blob';
  loadingInstance = ElLoading.service({
    lock: true,
    text: '正在下载，请稍候...',
    background: 'rgba(0, 0, 0, 0.5)',
  })
  return config;
});

requestFile.interceptors.response.use(
  (response) => {
    const res = response.data;
    const content = response.headers['content-disposition'] || 'filename=下载文件.xlsx'
    const filename = decodeURIComponent(content.split("filename=")[1])
    if (loadingInstance) {
      loadingInstance.close()
    }
    const blob = new Blob([res], {
      type: response.headers['content-type'] //文件下载类型
    });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename; // 自定义文件名
    link.click();
    return res
  },
  (err) => {
    ElNotification({
      message: '操作失败，请联系管理员',
      type: 'error',
    })
    if (loadingInstance) {
      loadingInstance.close()
    }
  }
);


export default service;
