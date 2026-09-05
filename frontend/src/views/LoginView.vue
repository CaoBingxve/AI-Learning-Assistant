<template>
  <div class="loginView">
    <h1>AI Learning Assistant</h1>

    <h2>登录</h2>

    <div>
      <label>用户名：</label>

      <input v-model="username" type="text" placeholder="请输入用户名" />
    </div>


    <div>
      <label>密码：</label>

      <input v-model="password" type="password" placeholder="请输入密码" />
    </div>


    <button @click="login" :disabled="loading">
      {{ loading ? '登录中...' : '登录' }}
    </button>


    <p v-if="errorMessage">
      {{ errorMessage }}
    </p>
  </div>
</template>

<script setup lang="ts" name="loginView">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useUserStore } from '@/stores/user'
import { loginApi } from '../api/user'

const userStore = useUserStore()

const router = useRouter()
const username = ref('')
const password = ref('')

const errorMessage = ref('')
const loading = ref(false)

async function login() {
  errorMessage.value = ''

  if (!username.value || !password.value) {
    errorMessage.value = '请输入用户名和密码'
    return
  }

  try {
    loading.value = true
    const response = await loginApi({
      username: username.value,
      password: password.value
    })

    // 获取返回值的token
    // 将token存储到本地
    userStore.setToken(response.data.access_token)

    await router.push('/home')
  } catch (error) {
    if (axios.isAxiosError(error)) {
      errorMessage.value =
        error.response?.data?.detail
        ?? '登录失败'
    } else {
      errorMessage.value = '登录失败'
    }
  } finally {
    loading.value = false
  }
}

</script>

<style scoped></style>