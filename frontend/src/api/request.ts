import axios, {
  type AxiosError
} from 'axios'


/**
 * 防止多个接口同时返回 401 时，
 * 重复执行跳转登录页。
 */
let isRedirectingToLogin = false


const request = axios.create({

  // 后端地址
  baseURL: 'http://127.0.0.1:8001',

  /*
   * Copilot / RAG 响应可能比较慢，
   * 所以这里不要再使用 10 秒。
   */
  timeout: 120000

})


/* ========================================
   Request Interceptor
   每次请求之前自动携带 JWT
======================================== */

request.interceptors.request.use(

  (config) => {

    const token =
      localStorage.getItem('token')


    if (token) {

      config.headers.Authorization =
        `Bearer ${token}`
    }


    return config
  },


  (error) => {

    return Promise.reject(error)
  }

)


/* ========================================
   Response Interceptor
   统一处理响应错误
======================================== */

request.interceptors.response.use(

  /*
   * 正常响应直接返回
   */
  (response) => {

    return response
  },


  /*
   * 请求发生错误
   */
  (error: AxiosError) => {

    const status =
      error.response?.status

    const url =
      error.config?.url ?? ''


    /*
     * 登录、注册接口属于公开接口。
     *
     * 登录时用户名密码错误可能返回 401，
     * 这个 401 不能被判断成“JWT过期”。
     */
    const isPublicAuthRequest =
      url.includes('/users/login')
      ||
      url.includes('/users/register')


    /*
     * 非登录/注册接口返回 401
     *
     * 一般意味着：
     * - Token过期
     * - Token无效
     * - 当前认证状态失效
     */
    if (
      status === 401
      &&
      !isPublicAuthRequest
    ) {

      /*
       * 先删除失效 Token
       */
      localStorage.removeItem(
        'token'
      )


      /*
       * 给 LoginView 留一个
       * 一次性提示。
       */
      sessionStorage.setItem(
        'auth_message',
        '登录状态已过期，请重新登录。'
      )


      /*
       * 防止：
       *
       * records → 401
       * currentUser → 401
       * chat → 401
       *
       * 多个请求同时触发多个跳转。
       */
      if (
        !isRedirectingToLogin
        &&
        window.location.pathname
          !== '/auth/login'
      ) {

        isRedirectingToLogin = true


        /*
         * 使用 replace 而不是 href：
         *
         * 不把失效页面继续留在
         * 浏览器历史记录里。
         */
        window.location.replace(
          '/auth/login'
        )
      }
    }


    return Promise.reject(error)
  }

)


export default request