import { useUserStore } from "@/stores/user";
import { createRouter, createWebHistory } from "vue-router";

const router=createRouter({
  history: createWebHistory(),
  routes: [
    {
      name: 'login',
      path: '/login',
      component:()=>import('@/views/LoginView.vue')
    },
    {
      name: 'register',
      path: '/register',
      component: () =>import('@/views/RegisterView.vue')
    },
    {
      name: 'home',
      path: '/home',
      component: ()=>import('@/views/HomeView.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      name: 'records',
      path: '/records',
      component: ()=>import('@/views/RecordView.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      name: 'chat',
      path: '/chat',
      component: ()=>import('@/views/ChatView.vue'),
      meta: {
        requiresAuth: true
      }
    }
  ]
})
router.beforeEach((to) => {
  const userStore=useUserStore()

  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    return { name: "login" };
  }

  // if ((to.name === 'login' || to.name === 'register')
  //   && userStore.isLoggedIn) {
  //   return { name: "home" };
  // }

  return true;
})

export default router