import request from '@/utils/request'
export function taskList(params = {}) {
  return request({
    url: `/tasks/list`,
    method: "get",
    params,
  });
}
export function addtask(params = {}) {
  return request({
    url: `/tasks/create`,
    method: "post",
    data: params,
  });
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