import request from "@/utils/request";
import axios from "axios";
// 书籍管理
export const booksApi = {
    getBooksList(params) {
        // return request({
        //   url: `/book/books-list`,
        //   method: "get",
        //   params,
        // });
        return axios.get(`/api/get_communities`, {
            params: {
                "page": params.page,
                "limit": params.limit,
                "name": params.name,
                "introduction": params.introduction,
                "startTime": params.startTime,
                "endTime": params.endTime
            }
        });
    },
    addCommunity(data) {
        return axios.post(`/api/add_community`, data);
    },
    getBookInfo(id) {
        return request({
            url: `/book/books/${id}`,
            method: "get",
        });
    },
    putBookInfo(data, id) {
        return request({
            url: `/book/books/${id}`,
            method: "put",
            data
        });
    },
    deleteCommunity(params: {}) {
        return axios.post(`/api/delete_community`, params)
    },
    checkQuanzi(name) {
        return axios.get(`/api/check_community?title=${name}`);
    },

    getTipInfo(id) {
        return axios.get(`/api/get_tipList?id=${id}`);
    },

    addNewPost(data = {}) {
        return axios.post("/api/add_tip", data)
    },
    checkBook(params) {
        return axios.get('/api/check_book', {
            params: {
                name: params.name,
                author: params.author
            }
        })
    },
    addBook(params) {
        return axios.post('/api/add_book', params)
    },
    deleteBook(params) {
        return axios.post(`/api/delete_book`, params)
    },
}
// 借书管理
export const borrowerApi = {
    getBorrowerList(params = {}) {
        return request({
            url: `/book/borrower-list`,
            method: "get",
            params,
        });
    },
    getBorrowerInfo(id) {
        return request({
            url: `/book/borrower/${id}`,
            method: "get",
        });
    },
    putBorrowerInfo(data, id) {
        return request({
            url: `/book/borrower/${id}`,
            method: "put",
            data
        });
    },
    deleteBorrowerInfo(id) {
        return request({
            url: `/book/borrower/${id}`,
            method: "delete",
        });
    },
    addBorrower(data) {
        return request({
            url: `/book/borrower/create`,
            method: "post",
            data
        });
    },
}




