import request from "@/utils/request";
import axios from "axios";

export const ancientPoetryApi = {
    getAncientPoetryList(params) {
        return axios.get('/api/get_bookDetailList', {
            params: {
                page: params.page,
                limit: params.limit,
                title: params.title,
                author: params.author,
                introduction: params.introduction,
                tag: params.tag
            },
        })
    },
    getBookFromDouBan(params) {
        return axios.post('/api/dig_book', params)
    },
    downLoadBooks(user_id) {
        return axios.get(`/api/downLoad_books?user_id=${user_id}`)
    }
}
export const ancientBooksApi = {
    getAncientBooksList(param) {
        return axios.get('/api/get_books', {
            params:
                {
                    "name": param.name,
                    "page": param.page,
                    "limit": param.limit
                }
        })
    },
    getAncientBooksInfo(params) {
        return axios.get(`/api/get_bookInfo?id=${params['id']}&user_id=${params['user_id']}`)
    },
    addNewReview(params = {}) {
        return axios.post(`/api/add_bookComment`, params)
    },
    addToFavorites(params = {}) {
        return axios.post('/api/add_favourite', params)
    },
    removeFromFavorites(params = {}) {
        return axios.post('/api/remove_favourite', params)
    }
}






