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
import { computed, onMounted, ref, watchEffect } from 'vue';
import { socket } from '@/main'

export default {
  setup() {
    const text = ref('')
    const connected = ref(false)

    function send() {
      socket.emit('ping', text.value)
    }

    socket.on('connect', () => {
      console.log("connected", socket.connected)
      connected.value = true
    })

    

    return {send, text, connected}
  }
}
</script>
