import request from '@/utils/request'
export function getPoetryCountTotal() {
  return request({
    url: `/ancient/poetry/count`,
    method: "get",
  });
}
