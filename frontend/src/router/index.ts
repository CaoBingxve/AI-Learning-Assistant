import {
  createRouter,
  createWebHistory
} from 'vue-router'

import {
  useUserStore
} from '@/stores/user'


const router = createRouter({

  history: createWebHistory(),

  routes: [

    // =========================
    // 登录 / 注册区域
    // =========================
    {
      path: '/auth',

      component: () =>
        import('@/layouts/AuthLayout.vue'),

      children: [

        {
          path: '',
          redirect: {
            name: 'login'
          }
        },

        {
          path: 'login',
          name: 'login',

          component: () =>
            import('@/views/LoginView.vue')
        },

        {
          path: 'register',
          name: 'register',

          component: () =>
            import('@/views/RegisterView.vue')
        }

      ]
    },


    // 兼容旧地址
    {
      path: '/login',
      redirect: '/auth/login'
    },

    {
      path: '/register',
      redirect: '/auth/register'
    },


    // =========================
    // 登录后的系统区域
    // =========================
    {
      path: '/',

      component: () =>
        import('@/layouts/MainLayout.vue'),

      meta: {
        requiresAuth: true
      },

      children: [

        {
          path: '',
          redirect: {
            name: 'home'
          }
        },

        {
          path: 'home',
          name: 'home',

          component: () =>
            import('@/views/HomeView.vue')
        },

        {
          path: 'records',
          name: 'records',

          component: () =>
            import('@/views/RecordView.vue')
        },

        {
          path: 'chat',
          name: 'chat',

          component: () =>
            import('@/views/ChatView.vue')
        }

      ]
    }

  ]
})


router.beforeEach((to) => {

  const userStore =
    useUserStore()


  // 未登录访问系统页面
  if (
    to.meta.requiresAuth &&
    !userStore.isLoggedIn
  ) {

    return {
      name: 'login'
    }
  }


  // 已登录不能重新访问登录/注册页
  if (
    (
      to.name === 'login' ||
      to.name === 'register'
    )
    &&
    userStore.isLoggedIn
  ) {

    return {
      name: 'home'
    }
  }


  return true
})


export default router