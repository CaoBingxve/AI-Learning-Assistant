<template>
  <h1>AI Learning Assistant</h1>
  <h2>
    欢迎回来，{{ userStore.currentUser?.username }}
  </h2>
  <button @click="showRecords">查看学习记录</button>
  <button @click="chatAI">学习助手</button>
  <button @click="logout">
    退出登录
  </button>
</template>

<script setup lang="ts" name="homeView">
import { useUserStore } from '@/stores/user';
import { useRouter } from 'vue-router';

const userStore = useUserStore()
const router = useRouter()

function logout() {
  userStore.logout()

  router.push('/login')
}

function showRecords() {
  router.push('/records')
}
function chatAI() {
  router.push('/chat')
}
</script>

<style scoped></style>