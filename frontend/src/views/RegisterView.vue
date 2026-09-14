<template>
  <div class="registerView">
    <h2>注册</h2>

    <div>
      <label>用户名：</label>

      <input v-model="username" type="text" placeholder="请输入用户名" />
    </div>


    <div>
      <label>密码：</label>

      <input v-model="password" type="password" placeholder="请输入密码" />
    </div>


    <div>
      <label>确认密码：</label>

      <input v-model="confirmPassword" type="password" placeholder="请再次输入密码" />
    </div>


    <button @click="handleRegister" :disabled="loading">
      {{ loading ? '注册中...' : '注册' }}
    </button>


    <p v-if="errorMessage" class="error">
      {{ errorMessage }}
    </p>


    <p>
      已有账号？

      <RouterLink to="/login">
        去登录
      </RouterLink>
    </p>

  </div>
</template>

<script setup lang="ts" name="registerView">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { registerApi } from '@/api/user'

const router = useRouter()

const username = ref('')
const password = ref('')
const confirmPassword = ref('')

const loading = ref(false)
const errorMessage = ref('')


async function handleRegister() {
  errorMessage.value = ''
  const usernameValue = username.value.trim()
  if (usernameValue.length < 3 || usernameValue.length > 20) {
    errorMessage.value = '用户名长度需要在 3～20 个字符之间'
    return
  }

  if (password.value.length < 6 || password.value.length > 30) {
    errorMessage.value = '密码长度需要在 6～30 个字符之间'
    return
  }
  if (!usernameValue || !password.value || !confirmPassword.value) {
    errorMessage.value = '请填写完整信息'
    return
  }

  if (password.value !== confirmPassword.value) {
    errorMessage.value = '两次输入的密码不一致'
    return
  }
  if (loading.value) {
    return
  }
  loading.value = true

  try {
    await registerApi({
      username: usernameValue,
      password: password.value
    })

    router.push('/login')
  } catch (error) {
    errorMessage.value = '注册失败，请稍后重试'
  } finally {
    loading.value = false
  }
}

</script>

<style scoped></style>