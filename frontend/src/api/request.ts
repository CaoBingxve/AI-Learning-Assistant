import axios, { AxiosError } from "axios";

const request = axios.create({
  baseURL: 'http://127.0.0.1:8001',
  timeout:10000
})

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    // 在发送请求之前做些什么
    const token = localStorage.getItem('token');  
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    // 它表示允许继续发送请求，如果不返回config，axios就会认为请求被中断，从而不会发送请求
    return config;
  }
  , (error) => {
    // 对请求错误做些什么
    return Promise.reject(error);
  } 
)

// 响应拦截器
request.interceptors.response.use(
  (response) => {
    // 请求成功，直接返回完整的数据
    return response
  },
  (error:AxiosError) => {
    const status = error.response?.data
    
    const url = error.config?.url
    
    // 登录接口自己处理“用户名密码错误”
    const isLoginRequest=url?.includes('users/login')

    // 如果不是登录接口，但是返回401
    // 那么说明登录无效或者过期了
    if (status === 401 && !isLoginRequest) {
      localStorage.removeItem('token')

      if (
        window.location.pathname !=='/login'
      ) {
        window.location.href='/login'
      }
    }

    return Promise.reject(error)
  }
)


export default request