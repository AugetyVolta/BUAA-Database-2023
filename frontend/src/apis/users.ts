import service from '@/utils/request'
import axios from "axios";

axios.defaults.maxContentLength = 10000000;

export function getVerificationCode() {
    return service({
        url: `/users/code`,
        method: "get",
    });
}

export function register(data = {}) {
    return axios.post("/api/add_user", data)
}

export function login(data = {}) {
    return axios.post("/api/user_login", data)
}

export function checkUserAccount(account) {
    return axios.get(`/api/check_user?account=${account}`)
}

export function changePassword(data = {}) {
    return axios.post(`/api/change_password`, data)
}

export function modifyUserData(data = {}) {
    return axios.post('/api/modify_userdata', data)
}

export function getUserReport(account) {
    return axios.get(`/api/getReport?account=${account}`)
}
