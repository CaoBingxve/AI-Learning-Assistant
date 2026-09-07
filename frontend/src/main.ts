import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import { useUserStore } from './stores/user'


async function bootstrap() {

  const app = createApp(App)

  const pinia = createPinia()

  // 这里面的顺序很重要
  // 先注册Pinia
  app.use(pinia)


  // 获取userStore
  const userStore =
    useUserStore(pinia)


  // 恢复登录状态
  await userStore.initializedAuth()


  // 再注册Router
  app.use(router)


  // 挂载Vue
  app.mount('#app')
}


bootstrap()