<template>
  <div class="home">
    <span class="title">{{ $t('home-race') }}</span>
    <v-input v-model="text" placeholder=""/>
    <v-button @click="send">Send</v-button>
    {{connected}}
    <router-link to="/race">Race</router-link>
  </div>
</template>

<script lang="ts">
import { computed, ref } from 'vue';
import { socket } from '@/main'

export default {
  setup() {
    const text = ref('')
    const connected = ref(false)
    socket.on('error', () => {
      console.log("Is Connected")
      connected.value = true
    })

    function send() {
      socket.emit('ping', text.value)
    }

    return {send, text, connected}
  }
}
</script>
