import {createRouter, createWebHashHistory, createWebHistory, RouteRecordRaw} from 'vue-router'
import {ElNotification} from 'element-plus'
import MainView from '@/layout/indexView.vue'

const hidden: boolean = true

const routes: Array<RouteRecordRaw> = [
    {
        path: '/',
        name: 'App',
        component: MainView,
        meta: {
            title: "书缘社",
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
                path: '/community/communities',
                name: 'community',
                meta: {
                    title: "知音阁",
                    icon: "Memo"
                },
                component: () => import('@/views/book-store/IndexView.vue'),
                // children: [
                //     // {
                //     //     path: '/book-store/books',
                //     //     name: 'books',
                //     //     meta: {
                //     //         title: "书籍管理",
                //     //         icon: "Memo"
                //     //     },
                //     //     component: () => import('@/views/book-store/IndexView.vue')
                //     // },
                //     {
                //         path: '/book-store/books/communities',
                //         name: 'tipsDetail',
                //         meta: {
                //             title: "相关帖子",
                //             parent: "书籍管理",
                //             parentPath: "/book-store/books/",
                //             hidden
                //         },
                //         component: () => import('@/views/book-store/page/tipDetail.vue'),
                //     },
                //     {
                //         path: '/book-store/books/tips',
                //         name: 'commentDetail',
                //         meta: {
                //             title: "评论区",
                //             parent: "书籍管理",
                //             parentPath: "/book-store/books/",
                //             hidden
                //         },
                //         component: () => import('@/views/book-store/page/commentDetail.vue'),
                //     },
                // ],

            },
            {
                path: '/community/tips',
                name: 'tipsDetail',
                meta: {
                    title: "相关帖子",
                    parent: "知音阁",
                    parentPath: "/community/communities",
                    hidden
                },
                component: () => import('@/views/book-store/page/tipDetail.vue'),
            },
            {
                path: '/community/tip/comments',
                name: 'commentDetail',
                meta: {
                    title: "评论区",
                    parent: "相关帖子",
                    parentPath: "/community/communities",
                    hidden
                },
                component: () => import('@/views/book-store/page/commentDetail.vue'),
            },
            {
                path: '/tasks',
                name: 'tasks',
                meta: {
                    title: "静审轩",
                    icon: "SetUp"
                },
                component: () => import('@/views/tasks/IndexView.vue')
            },
            {
                path: "/library",
                name: 'library',
                redirect: "/library/list",
                meta: {
                    title: "书韵轩",
                    icon: "Reading"
                },
                children: [
                    {
                        path: '/library/list',
                        name: 'bookList',
                        meta: {
                            title: "翰墨阁",
                            icon: "Document"
                        },
                        component: () => import('@/views/ancient-poetry/IndexView.vue'),
                    },
                    {
                        path: '/library/books',
                        name: 'books',
                        meta: {
                            title: "文轩阁",
                            icon: "Notebook"
                        },
                        component: () => import('@/views/ancient-poetry/AncientBooks.vue'),

                    },
                    {
                        path: '/library/books/book',
                        name: 'bookDetail',
                        meta: {
                            title: "书籍详情",
                            parent: "文轩阁",
                            parentPath: "/library/books",
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
