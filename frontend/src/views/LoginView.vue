<template>
  <div class="auth-view">

    <!-- 标题 -->
    <div class="auth-header">
      <div class="auth-badge">
        欢迎回来
      </div>

      <h2>
        登录你的账号
      </h2>

      <p>
        继续记录学习，让 Copilot 更了解你的学习过程。
      </p>
    </div>


    <!-- Token 过期提示 -->
    <div v-if="authMessage" class="message-box warning-message">
      <span class="message-icon">!</span>

      <span>
        {{ authMessage }}
      </span>
    </div>


    <!-- 注册成功提示 -->
    <div v-if="successMessage" class="message-box success-message">
      <span class="message-icon">✓</span>

      <span>
        {{ successMessage }}
      </span>
    </div>


    <!-- 登录错误 -->
    <div v-if="errorMessage" class="message-box error-message">
      <span class="message-icon">!</span>

      <span>
        {{ errorMessage }}
      </span>
    </div>


    <!-- 表单 -->
    <form class="auth-form" @submit.prevent="handleLogin">

      <div class="form-group">

        <label for="username">
          用户名
        </label>

        <div class="input-wrapper">

          <span class="input-icon">
            U
          </span>

          <input id="username" v-model="username" type="text" autocomplete="username" placeholder="请输入用户名" />

        </div>

      </div>


      <div class="form-group">

        <div class="label-row">

          <label for="password">
            密码
          </label>

        </div>


        <div class="input-wrapper">

          <span class="input-icon">
            •
          </span>

          <input id="password" v-model="password" :type="showPassword ? 'text' : 'password'"
            autocomplete="current-password" placeholder="请输入密码" />


          <button type="button" class="password-toggle" @click="showPassword = !showPassword">
            {{
              showPassword
                ? '隐藏'
                : '显示'
            }}
          </button>

        </div>

      </div>


      <button type="submit" class="submit-button" :disabled="loading">
        <span v-if="loading">
          正在登录...
        </span>

        <span v-else>
          登录
        </span>
      </button>

    </form>


    <!-- 底部 -->
    <div class="auth-footer">

      <span>
        还没有账号？
      </span>

      <RouterLink :to="{ name: 'register' }">
        创建账号
      </RouterLink>

    </div>

  </div>
</template>


<script setup lang="ts">

import {
  onMounted,
  ref
} from 'vue'

import {
  useRouter
} from 'vue-router'

import {
  loginApi
} from '@/api/user'

import {
  useUserStore
} from '@/stores/user'


const router =
  useRouter()

const userStore =
  useUserStore()


const username =
  ref('')

const password =
  ref('')

const showPassword =
  ref(false)

const loading =
  ref(false)

const errorMessage =
  ref('')

const authMessage =
  ref('')

const successMessage =
  ref('')


async function handleLogin() {

  errorMessage.value = ''

  const usernameValue =
    username.value.trim()


  if (
    !usernameValue ||
    !password.value
  ) {

    errorMessage.value =
      '请输入用户名和密码。'

    return
  }


  if (loading.value) {
    return
  }


  loading.value = true


  try {

    const response =
      await loginApi({

        username:
          usernameValue,

        password:
          password.value
      })


    userStore.setToken(
      response.data.access_token
    )


    await userStore
      .fetchCurrentUser()


    await router.push({
      name: 'home'
    })


  } catch (error) {

    console.error(
      '登录失败：',
      error
    )

    errorMessage.value =
      '用户名或密码错误，请重新输入。'

  } finally {

    loading.value = false
  }
}


onMounted(() => {

  /*
   * JWT过期提示
   */
  const auth =
    sessionStorage.getItem(
      'auth_message'
    )


  if (auth) {

    authMessage.value = auth

    sessionStorage.removeItem(
      'auth_message'
    )
  }


  /*
   * 注册成功提示
   */
  const registerMessage =
    sessionStorage.getItem(
      'register_message'
    )


  if (registerMessage) {

    successMessage.value =
      registerMessage

    sessionStorage.removeItem(
      'register_message'
    )
  }

})

</script>


<style scoped src="../assets/styles/auth-form.css"></style>