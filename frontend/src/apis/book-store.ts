import request from "@/utils/request";
// 书籍管理
export const booksApi = {
  getBooksList(params = {}) {
    return request({
      url: `/book/books-list`,
      method: "get",
      params,
    });
  },
  addBook(data) {
    return request({
      url: `/book/books/create`,
      method: "post",
      data
    });
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
  deleteBookInfo(id) {
    return request({
      url: `/book/books/${id}`,
      method: "delete",
    });
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




