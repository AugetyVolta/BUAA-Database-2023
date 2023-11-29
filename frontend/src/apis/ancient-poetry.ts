import request from "@/utils/request";
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
    return request({
      url: `/ancient/books`,
      method: "get",
      params,
    });
  },
  getAncientBooksInfo(id) {
    return request({
      url: `/ancient/books/${id}`,
      method: "get",
    });
  },
}






