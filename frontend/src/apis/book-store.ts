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
    editBook(params) {
        return axios.post('/api/edit_book', params)
    },
    uploadBooks(params) {
        return axios.post('/api/upload_book', params)
    },
    deleteBook(params) {
        return axios.post(`/api/delete_book`, params)
    },

    addSupport(id, user_id) {
        return axios.get(`/api/add_support?tip_id=${id}&id=${user_id}`);
    },

    addUnsupported(id, user_id) {
        return axios.get(`/api/add_unsupported?tip_id=${id}&id=${user_id}`)
    },

    deleteTipInfo(params) {
        return axios.post(`/api/delete_tip`, params)
    },

    getCommentInfo(id) {
        return axios.get(`/api/get_commentList?id=${id}`)
    },

    addComment(params) {
        return axios.post(`/api/add_comment`, params)
    },
    deleteComment(params) {
        return axios.post(`/api/delete_comment`, params)
    }
}

// 借书管理
export const userApi = {
    getUserList(params = {}) {
        return axios.post('/api/get_userList', params)
    },
    getUserLogList(params = {}) {
        return axios.post('/api/get_userLogList', params)
    },
    modify_userPrivilege(params: {}) {
        return axios.post('/api/modify_userPrivilege', params)
    },
    downloadUserLog(params: {}) {
        return axios.post('/api/downloadUserLog', params)
    }
}




