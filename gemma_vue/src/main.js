import { createApp } from 'vue'
import App from './App.vue'
import io from 'socket.io-client'
import ElementPlus from 'element-plus'
import "element-plus/dist/index.css"
import axios from 'axios'

// 创建 WebSocket 连接
const socket = io('http://localhost:5000')

const app = createApp(App)

// 将 socket 注入到所有组件中
app.config.globalProperties.$socket = socket
app.use(ElementPlus)

// 设置 axios 的默认配置
axios.defaults.baseURL = 'http://localhost:5000';
axios.defaults.timeout = 10000; // 设置请求超时
app.config.globalProperties.$axios = axios;

app.mount('#app')
