import {createRouter, createWebHashHistory, createWebHistory, RouteRecordRaw} from 'vue-router'
import {ElNotification} from 'element-plus'
import MainView from '@/layout/indexView.vue'
import {reactive, ref} from "vue/dist/vue";

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
                component: () => import('@/views/community/IndexView.vue'),
                // children: [
                //     // {
                //     //     path: '/community/books',
                //     //     name: 'books',
                //     //     meta: {
                //     //         title: "书籍管理",
                //     //         icon: "Memo"
                //     //     },
                //     //     component: () => import('@/views/community/IndexView.vue')
                //     // },
                //     {
                //         path: '/community/books/communities',
                //         name: 'tipsDetail',
                //         meta: {
                //             title: "相关帖子",
                //             parent: "书籍管理",
                //             parentPath: "/community/books/",
                //             hidden
                //         },
                //         component: () => import('@/views/community/page/tipDetail.vue'),
                //     },
                //     {
                //         path: '/community/books/tips',
                //         name: 'commentDetail',
                //         meta: {
                //             title: "评论区",
                //             parent: "书籍管理",
                //             parentPath: "/community/books/",
                //             hidden
                //         },
                //         component: () => import('@/views/community/page/commentDetail.vue'),
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
                component: () => import('@/views/community/page/tipDetail.vue'),
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
                component: () => import('@/views/community/page/commentDetail.vue'),
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
                        component: () => import('@/views/book/IndexView.vue'),
                    },
                    {
                        path: '/library/books',
                        name: 'books',
                        meta: {
                            title: "文轩阁",
                            icon: "Notebook"
                        },
                        component: () => import('@/views/book/Library.vue'),

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
                        component: () => import('@/views/book/page/bookDetail.vue'),
                    },
                ],

            },
            {
                path: '/user-manager',
                name: 'manage',
                meta: {
                    title: "用户管理",
                    icon: "Management"
                },
                component: () => import('@/views/Manage.vue')
            },
            {
                path: '/user-log',
                name: 'log',
                meta: {
                    title: "用户日志",
                    icon: "List"
                },
                component: () => import('@/views/UserLog.vue')
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
    routes: routes
})

router.beforeEach((to, from, next) => {
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
