import { createRouter, createWebHashHistory, createWebHistory, RouteRecordRaw } from 'vue-router'
import { ElNotification } from 'element-plus'
import MainView from '@/layout/indexView.vue'
const hidden: boolean = true

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'App',
    component: MainView,
    meta: {
      title: "星域平台管理系统",
    },
    redirect: "/home",
    children: [
      {
        path: '/home',
        name: 'home',
        meta: {
          title: "系统首页",
          icon: "HomeFilled"
        },
        component: () => import('@/views/HomeView.vue')
      },
      {
        path: '/tasks',
        name: 'tasks',
        meta: {
          title: "任务管理",
          icon: "SetUp"
        },
        component: () => import('@/views/tasks/IndexView.vue')
      },
      {
        path: "/book-store",
        name: 'book-store',
        redirect: "/book-store/books",
        meta: {
          title: "书店管理",
          icon: "School"
        },
        children: [
          {
            path: '/book-store/books',
            name: 'books',
            meta: {
              title: "书籍管理",
              icon: "Memo"
            },
            component: () => import('@/views/book-store/IndexView.vue')
          },
          {
            path: '/book-store/books/tips',
            name: 'tipsDetail',
            meta: {
              title: "相关帖子",
              parent: "书籍管理",
              parentPath: "/book-store/books/",
              hidden
            },
            component: () => import('@/views/book-store/page/tipDetail.vue'),
          },
          {
            path: '/book-store/borrow-books',
            name: 'BorrowBooks',
            meta: {
              title: "借书管理",
              icon: "Collection"
            },
            component: () => import('@/views/book-store/BorrowBooks.vue')
          },
        ],

      },
      {
        path: "/ancient",
        name: 'ancient',
        redirect: "/ancient/poetry",
        meta: {
          title: "古文学习",
          icon: "Reading"
        },
        children: [
          {
            path: '/ancient/poetry',
            name: 'ancientPoetry',
            meta: {
              title: "古诗学习",
              icon: "Document"
            },
            component: () => import('@/views/ancient-poetry/IndexView.vue'),
          },
          {
            path: '/ancient/poetry/detail',
            name: 'ancientPoetryDetail',
            meta: {
              title: "古诗详情",
              parent: "古诗学习",
              parentPath: "/ancient/poetry",
              hidden
            },
            component: () => import('@/views/ancient-poetry/page/poetryDetail.vue'),
          },
          {
            path: '/ancient/books',
            name: 'ancientBooks',
            meta: {
              title: "古籍学习",
              icon: "Notebook"
            },
            component: () => import('@/views/ancient-poetry/AncientBooks.vue'),

          },
          {
            path: '/ancient/poetry/book',
            name: 'ancientBookDetail',
            meta: {
              title: "古籍详情",
              parent: "古籍学习",
              parentPath: "/ancient/books",
              hidden
            },
            component: () => import('@/views/ancient-poetry/page/bookDetail.vue'),
          },
        ],

      },
      {
        path: '/user-center',
        name: 'UserCenter',
        meta: {
          title: "用户中心",
          icon: "UserFilled"
        },
        component: () => import('@/views/UserCenter.vue')
      },
    ]
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/Login.vue')
  },

]

const router = createRouter({
  history: createWebHashHistory(process.env.BASE_URL),
  routes
})
router.beforeEach((to, from, next) => {
  //console.log(localStorage.getItem("token"))
  console.log(to.path)
  if (!localStorage.getItem("token") && to.path !== '/login') {
    next("/login");
    ElNotification.error({
      title: '令牌为空',
      message: '认证信息不可用，请重新登录',
      duration: 0
    });
  } else {
    next()
  }
});

export default router
