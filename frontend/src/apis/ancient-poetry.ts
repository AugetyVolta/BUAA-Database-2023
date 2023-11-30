import request from "@/utils/request";
import axios from "axios";

export const ancientPoetryApi = {
    getAncientPoetryList(params = {}) {
        return request({
            url: `/ancient/poetry`,
            method: "get",
            params,
        });
    },
    getAncientPoetryInfo(id) {
        return request({
            url: `/ancient/poetry/${id}`,
            method: "get",
        });
    },
    getFamousList(params = {}) {
        return request({
            url: `/ancient/famous`,
            method: "get",
            params,
        })
    },
    getFamousInfo(id) {
        return request({
            url: `/ancient/famous/${id}`,
            method: "get",
        })
    }
}
export const ancientBooksApi = {
    getAncientBooksList(params = {}) {
        return axios.get('/api/get_books', params)
    },
    getAncientBooksInfo(id) {
        return axios.get(`/api/get_bookInfo?id=${id}`)
    },

    addNewReview(params = {}) {
        return axios.post(`/api/add_bookComment`, params)
    }

}






