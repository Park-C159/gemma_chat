<template>
  <div class="code-block-container">
    <div class="code-block-header">
      <span class="code-block-lang">{{ language }}</span>
      <button @click="copyCode" class="copy-button">复制</button>
    </div>
    <pre><code ref="code" :class="`language-${language}`">{{ code }}</code></pre>
  </div>
</template>

<script>
import hljs from "highlight.js";

export default {
  props: {
    code: {
      type: String,
      required: true,
    },
    language: {
      type: String,
      default: "plaintext",
    },
  },
  mounted() {
    this.highlightCode();
  },
  methods: {
    highlightCode() {
      hljs.highlightElement(this.$refs.code);
    },
    copyCode() {
      navigator.clipboard.writeText(this.code).then(() => {
        alert("代码已复制到剪贴板");
      });
    },
  },
};
</script>

<style scoped>
.code-block-container {
  position: relative;
  background: #272822;
  border-radius: 5px;
  margin-bottom: 16px;
  padding-top: 40px; /* 给标题留空间 */
}

.code-block-header {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 5px 10px;
  background: #333;
  border-top-left-radius: 5px;
  border-top-right-radius: 5px;
}

.code-block-lang {
  color: #f8f8f2;
  font-size: 12px;
  font-weight: bold;
}

.copy-button {
  background: #007bff;
  color: #fff;
  border: none;
  border-radius: 3px;
  padding: 3px 8px;
  cursor: pointer;
}

.copy-button:hover {
  background: #0056b3;
}

pre {
  margin: 0;
  padding: 10px;
  overflow-x: auto;
}
</style>
