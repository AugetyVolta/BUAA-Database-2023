import request from '@/utils/request'
import axios from "axios";
export function getPoetryCountTotal() {
  return request({
    url: `/ancient/poetry/count`,
    method: "get",
  });
}

export function  getRecommendedBooks() {
  return axios.post(`/api/getRecommendedBooks`)
}

export function getIdOfBook(param) {
  return axios.post(`/api/getIdOfBook`, param)
}
