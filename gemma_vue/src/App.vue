<template>
  <!--  <img alt="Vue logo" src="./assets/logo.png">-->
  <!--  <HelloWorld msg="Welcome to Your Vue.js App"/>-->
  <table></table>
  <ChatContent/>
</template>

<script>
// import HelloWorld from './components/HelloWorld.vue'
import ChatContent from './components/ChatContent.vue'

export default {
  name: 'App',
  components: {
    // HelloWorld,
    ChatContent,
  }
}
</script>

<style>
body, html, head, ul, li, p {
  margin: 0;
  padding: 0;
}

* {
  box-sizing: border-box;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

a {
  cursor: pointer;
}

h1, h2, h3, h4, h5 {
  margin: 0;
}
</style>
