import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import { getCurrentUserApi,type userInfo } from '@/api/user'
   
export const useUserStore = defineStore('user', () => {
  const currentUser = ref<userInfo|null>(null)
  
  const token = ref(
    localStorage.getItem('token')??''
  )

  const initailized=ref(false)

  // !! 的作用是把值转换为布尔值
  const isLoggedIn=computed(() => {
    return !!token.value
  })

  function setToken(newToken: string) {
    token.value = newToken
    localStorage.setItem('token',newToken)
  }

  async function fetchCurrentUser() {
    const response = await getCurrentUserApi()
    currentUser.value=response.data
  }

  // 应用启动时恢复登录状态
  async function initializedAuth() {
    // 没有Token，根本就不用请求后端数据
    if (!token.value) {
      currentUser.value = null
      initailized.value = true
      return
    }

    try {
      // 有token，重新去后端确认身份
      await fetchCurrentUser()
    } catch (error) {
      logout()
    } finally {
      initailized.value=true
    }
  }

  function logout() {
    currentUser.value = null
    token.value = ''
    localStorage.removeItem('token')
  }

  return {
    currentUser,
    token,
    initailized,
    isLoggedIn,
    setToken,
    fetchCurrentUser,
    logout,
    initializedAuth
  }
})