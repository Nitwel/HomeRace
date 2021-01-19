<template>
  <div class="home">
    <span class="title">{{ $t('home-race') }}</span>
    <v-input v-model="text" placeholder=""/>
    <v-button @click="send">Send</v-button>
  </div>
</template>

<script lang="ts">
import { ref } from 'vue';
import { socket } from '@/main'

export default {
  setup() {
    const text = ref('')

    function send() {
      socket.emit('ping', text.value)
    }

    return {send, text}
  }
}
</script>
