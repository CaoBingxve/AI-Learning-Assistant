import ChatView from "@/views/ChatView.vue";
import HomeView from "@/views/HomeView.vue";
import LoginView from "@/views/LoginView.vue";
import RecordView from "@/views/RecordView.vue";
import RegisterView from "@/views/RegisterView.vue";
import { createRouter, createWebHistory } from "vue-router";

export default createRouter({
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
      component:HomeView
    },
    {
      name: 'records',
      path: '/records',
      component:RecordView
    },
    {
      name: 'chat',
      path: '/chat',
      component:ChatView
    }
  ]
})