<template>
  <div class="auth-view">

    <!-- 标题 -->
    <div class="auth-header">

      <div class="auth-badge">
        开始使用
      </div>

      <h2>
        创建你的账号
      </h2>

      <p>
        建立个人学习空间，让 Copilot 开始了解你的学习轨迹。
      </p>

    </div>


    <!-- 错误 -->
    <div v-if="errorMessage" class="message-box error-message">
      <span class="message-icon">
        !
      </span>

      <span>
        {{ errorMessage }}
      </span>
    </div>


    <!-- 表单 -->
    <form class="auth-form" @submit.prevent="handleRegister">

      <!-- 用户名 -->
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


      <!-- 密码 -->
      <div class="form-group">

        <label for="password">
          密码
        </label>

        <div class="input-wrapper">

          <span class="input-icon">
            •
          </span>

          <input id="password" v-model="password" :type="showPassword
            ? 'text'
            : 'password'
            " autocomplete="new-password" placeholder="请输入密码" />


          <button type="button" class="password-toggle" @click="
            showPassword =
            !showPassword
            ">
            {{
              showPassword
                ? '隐藏'
                : '显示'
            }}
          </button>

        </div>

      </div>


      <!-- 确认密码 -->
      <div class="form-group">

        <label for="confirmPassword">
          确认密码
        </label>

        <div class="input-wrapper">

          <span class="input-icon">
            ✓
          </span>

          <input id="confirmPassword" v-model="confirmPassword" :type="showPassword
            ? 'text'
            : 'password'
            " autocomplete="new-password" placeholder="请再次输入密码" />

        </div>

      </div>


      <button type="submit" class="submit-button" :disabled="loading">
        {{
          loading
            ? '正在创建...'
            : '创建账号'
        }}
      </button>

    </form>


    <!-- 底部 -->
    <div class="auth-footer">

      <span>
        已经有账号？
      </span>

      <RouterLink :to="{ name: 'login' }">
        返回登录
      </RouterLink>

    </div>

  </div>
</template>


<script setup lang="ts">

import {
  ref
} from 'vue'

import {
  useRouter
} from 'vue-router'

import {
  registerApi
} from '@/api/user'


const router =
  useRouter()


const username =
  ref('')

const password =
  ref('')

const confirmPassword =
  ref('')

const showPassword =
  ref(false)

const loading =
  ref(false)

const errorMessage =
  ref('')


async function handleRegister() {

  errorMessage.value = ''


  const usernameValue =
    username.value.trim()


  /*
   * 1. 空值校验
   */
  if (
    !usernameValue ||
    !password.value ||
    !confirmPassword.value
  ) {

    errorMessage.value =
      '请填写完整的注册信息。'

    return
  }


  /*
   * 2. 把你原来已经验证成功的
   * 用户名长度判断放在这里
   *
   * 示例：
   *
   * if (...) {
   *   errorMessage.value =
   *     '用户名长度需要在 ... 之间'
   *   return
   * }
   */


  /*
   * 3. 把你原来的
   * 密码长度判断放在这里
   */


  /*
   * 4. 两次密码一致
   */
  if (
    password.value
    !==
    confirmPassword.value
  ) {

    errorMessage.value =
      '两次输入的密码不一致。'

    return
  }


  if (loading.value) {
    return
  }


  loading.value = true


  try {

    await registerApi({

      username:
        usernameValue,

      password:
        password.value
    })


    /*
     * 登录页显示一次
     * 注册成功提示
     */
    sessionStorage.setItem(
      'register_message',
      '账号创建成功，请登录。'
    )


    await router.push({
      name: 'login'
    })


  } catch (error) {

    console.error(
      '注册失败：',
      error
    )

    errorMessage.value =
      '注册失败，请检查用户名是否已存在或输入是否符合要求。'

  } finally {

    loading.value = false
  }
}

</script>


<style scoped src="../assets/styles/auth-form.css"></style>