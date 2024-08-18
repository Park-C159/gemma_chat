<template>
  <div id="app">
    <h1>Gemma大模型</h1>
    <div class="chat-container">
      <ul class="chat-log">
        <li v-for="(msg, index) in messages" :key="index" v-html="renderMarkdown(msg)" class="chat-message"></li>
      </ul>
    </div>

    <div class="input-container">
      <input v-model="message" @keyup.enter="sendMessage" placeholder="输入你的消息..." class="chat-input" />
      <el-button size="large" @click="sendMessage" class="send-button">发送</el-button>
    </div>
  </div>
</template>

<script>
import {marked} from "marked"

export default {
  data() {
    return {
      message: '',
      messages: [],
      partialMsg: "Gemma：\n",  // 当前正在接收的消息
    }
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
        this.partialMsg = 'Gemma：\n';  // 重置
      }
    });
  },
  methods: {
    sendMessage() {
      if (this.message.trim() !== '') {
        this.messages.push("用户：\n"+this.message + "<end_of_turn>");
        this.$socket.send(this.message);
        this.message = '';
      }
    },
    renderMarkdown(msg) {
      return marked(msg);
    }
  }
}

</script>

<style scoped>
#app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  text-align: center;
  margin-top: 40px;
}

.chat-container {
  width: 60%;
  margin: 0 auto;
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.chat-log {
  list-style-type: none;
  padding: 0;
  margin-bottom: 20px;
  max-height: 400px;
  overflow-y: auto;
}

.chat-message {
  padding: 10px;
  border-radius: 5px;
  margin-bottom: 10px;
  background-color: #ffffff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  text-align: left;
  white-space: pre-wrap;
}

.input-container {
  width: 60%;
  display: flex;
  justify-content: space-between;
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
  width: 8px;
}

.chat-log::-webkit-scrollbar-thumb {
  background-color: #007BFF;
  border-radius: 4px;
}
</style>
