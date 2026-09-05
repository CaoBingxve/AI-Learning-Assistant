import { defineStore } from 'pinia'
import {computed, ref} from 'vue'
   
export const useUserStore = defineStore('user', () => {
  const username = ref('')
  
  const token = ref(
    localStorage.getItem('token')??''
  )

  // !! 的作用是把值转换为布尔值
  const isLoggedIn=computed(() => {
    return !!token.value
  })

  function setToken(newToken: string) {
    token.value = newToken
    localStorage.setItem('token',newToken)
  }

  function logout() {
    username.value = ''
    token.value = ''
    localStorage.removeItem('token')
  }

  return {
    username,
    token,
    isLoggedIn,
    setToken,
    logout
  }
})