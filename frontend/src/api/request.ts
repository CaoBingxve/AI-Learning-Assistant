import axios from "axios";

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


export default request