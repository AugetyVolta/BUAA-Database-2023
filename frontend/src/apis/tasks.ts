import request from '@/utils/request'
import axios from "axios";
export function taskList(params = {}) {
  return axios.post(`/api/get_task`, params)
}

export function othertaskList(params = {}) {
  return axios.post(`/api/get_tip_status`, params)
}
export function acceptPost(param) {
  return axios.post(`/api/accept_tip`, param)
}

export function refusePost(param) {
  return axios.post(`/api/refuse_tip`, param)
}
export function updatetask(params = {}, id = null) {
  return request({
    url: `/tasks/update/${id}`,
    method: "put",
    data: params,
  });
}
export function deletetask(id = null) {
  return request({
    url: `/tasks/delete/${id}`,
    method: "delete",
  });
}
export function taskdetail(id = null) {
  return request({
    url: `/tasks/detail/${id}`,
    method: "get",
  });
}