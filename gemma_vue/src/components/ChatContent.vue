<template>
  <div id="content">
    <div class="title">
      Gemma大模型
    </div>
    <div class="chat-container">
      <ul class="chat-log">
        <li v-for="(msg, index) in messages" :key="index" v-html="renderMarkdown(msg)" class="chat-message"></li>
      </ul>
    </div>

    <div class="input-container">
      <input v-model="message" @keyup.enter="sendMessage" placeholder="输入你的消息..." class="chat-input"/>
      <el-button @click="refresh" size="large"><el-icon><Refresh /></el-icon></el-button>

      <el-button v-if="!isReciving" size="large" @click="sendMessage" class="send-button">发送</el-button>
      <el-button v-else size="large" type="primary" disabled>发送</el-button>
    </div>
  </div>
</template>

<script>
import {marked} from "marked"
import hljs from "highlight.js"
import "highlight.js/styles/monokai-sublime.css"
import { Refresh } from '@element-plus/icons-vue'


export default {
  data() {
    return {
      message: '',
      messages: [],
      partialMsg: "#### Gemma：\n",  // 当前正在接收的消息
      isReciving: false,
      isStop: true,
    }
  },
  components: {
    Refresh,
  },
  created() {
    this.loadHistory()

  },
  mounted() {
    // 监听 WebSocket 消息
    this.$socket.on('message', (msg) => {
      this.partialMsg += msg;

      if (this.messages.length === 0 || this.messages[this.messages.length - 1].endsWith("<end_of_turn>")) {
        this.messages.push(this.partialMsg);  // 开始新的消息

      } else {
        this.messages[this.messages.length - 1] = this.partialMsg;  // 更新当前正在显示的消息
      }

      if (msg.endsWith("<end_of_turn>")) {
        this.messages[this.messages.length - 1] = this.partialMsg.replace("<end_of_turn>", '');
        this.partialMsg = '#### Gemma：\n';  // 重置
        this.isReciving = false
      }
    });

    window.addEventListener("beforeunload", () => {
      this.stop_chat()
    })
  },
  updated() {
    this.scrollToBottom()
  },

  methods: {
    refresh(){
      this.$axios.delete("/restart_chat").then((response) => {
        let res = response.data;
        console.log(res);
        if (res.code === 200) {
          this.messages = []
        }
      })
    },
    loadHistory() {
      this.$axios.get("/history_chat").then((response) => {
        let res = response.data;
        if (res.code === 200){
          this.messages = res.data;
        }
      }).catch((error) => {
        console.log(error);
      })
    },

    stop_chat(){
      this.$axios.get("/stop_chat").then(res => {
        if (res.status === 200){
          this.isStop = true;
        }
      }).catch(err => {
        console.log(err);
      })
    },
    escapeMarkdown(text) {
      return text
          .replace(/&/g, "&amp;")
          .replace(/</g, "&lt;")
          .replace(/>/g, "&gt;")
          .replace(/"/g, "&quot;")
          .replace(/'/g, "&#039;")
          .replace(/\*/g, "&#42;")
          .replace(/_/g, "&#95;")
          .replace(/`/g, "&#96;")
          .replace(/\[/g, "&#91;")
          .replace(/]/g, "&#93;")
          .replace(/\(/g, "&#40;")
          .replace(/\)/g, "&#41;")
          .replace(/#/g, "&#35;");
    },
    sendMessage() {
      this.$axios.get("/start_chat").then(res => {
        console.log(res)

        if (res.status === 200){
          if (this.message.trim() !== '') {
            this.messages.push("#### 用户：\n" + this.escapeMarkdown(this.message) + "<end_of_turn>");
            this.isReciving = true
            this.$socket.send(this.message);
            this.message = '';
          }
        }
      }).catch(err => {
        console.log(err);
      })
    },
    renderMarkdown(msg) {
      const rendered = marked(msg);
      this.$nextTick(()=>{
        this.hanleHightLight()
      })
      return rendered
    },
    scrollToBottom() {
      const chatLog = this.$el.querySelector('.chat-log');
      chatLog.scrollTop = chatLog.scrollHeight;
    },
    hanleHightLight(){
      let blocks = document.querySelectorAll("pre code");
      blocks.forEach((block) => {
        // 检查是否已经存在复制按钮X
        if (!block.parentNode.querySelector(".copy-button")) {
          // 创建复制按钮
          const copyButton = document.createElement("span");
          copyButton.className = "copy-button";
          copyButton.innerText = "复制";
          block.parentNode.style.position = "relative";  // 确保父容器相对定位
          block.parentNode.appendChild(copyButton);

          // 添加复制功能
          copyButton.addEventListener("click", () => {
            const code = block.innerText;
            navigator.clipboard.writeText(code).then(() => {
              copyButton.innerText = "已复制";
              setTimeout(() => {
                copyButton.innerText = "复制";
              }, 2000);
            });
          });
        }

        hljs.highlightElement(block);

      });

    }
  },
}

</script>
<style>

.copy-button {
  position: absolute;
  top: 10px;
  right: 10px;
  border: none;
  border-radius: 4px;
  padding: 4px 8px;
  cursor: pointer;
  font-size: 12px;
  z-index: 10;
  color: #fff;
}
.copy-button:hover {
  color: #dddddd;
}

</style>

<style scoped>
#content {
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  text-align: center;
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
}

.chat-container {
  width: 100%;
  margin: 0 auto;
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  height: calc(100% - 50px - 2.5em - 10%);
}

.title {
  font-size: 2em;
  line-height: 2.5em;
  font-weight: 600;
}

.chat-log {
  list-style-type: none;
  padding: 0;
  height: 100%;
  overflow-y: auto;
}

.chat-message {
  padding: 10px 10px 10px 30px;
  border-radius: 5px;
  margin-bottom: 10px;
  background-color: #ffffff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  text-align: left;
  white-space: pre-wrap;
}

.input-container {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 50px;
}

.chat-input {
  flex-grow: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  margin-right: 10px;
}

.send-button {
  padding: 10px 20px;
  background-color: #007BFF;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.send-button:hover {
  background-color: #0056b3;
}

.chat-log::-webkit-scrollbar {
  width: 2px;
}

.chat-log::-webkit-scrollbar-thumb {
  background-color: #007BFF;
  border-radius: 4px;
}

pre {
  position: relative;
  padding-top: 30px; /* 为按钮腾出空间 */
}

</style>
