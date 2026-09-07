import { useUserStore } from "@/stores/user";
import ChatView from "@/views/ChatView.vue";
import HomeView from "@/views/HomeView.vue";
import LoginView from "@/views/LoginView.vue";
import RecordView from "@/views/RecordView.vue";
import RegisterView from "@/views/RegisterView.vue";
import { createRouter, createWebHistory } from "vue-router";

const router=createRouter({
  history: createWebHistory(),
  routes: [
    {
      name: 'login',
      path: '/login',
      component:LoginView
    },
    {
      name: 'register',
      path: '/register',
      component:RegisterView
    },
    {
      name: 'home',
      path: '/home',
      component: HomeView,
      meta: {
        requiresAuth: true
      }
    },
    {
      name: 'records',
      path: '/records',
      component: RecordView,
      meta: {
        requiresAuth: true
      }
    },
    {
      name: 'chat',
      path: '/chat',
      component:ChatView
    }
  ]
})
router.beforeEach((to) => {
  const userStore=useUserStore()

  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    return { name: "login" };
  }

  if (to.name === "login"  && userStore.isLoggedIn) {
    return { name: "home" };
  }

  return true;
})

export default router