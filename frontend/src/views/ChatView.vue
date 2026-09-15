<template>
  <div class="chat-view">

    <ChatHeader @new-chat="newConversation" />

    <ChatMessageList :messages="messages" :loading="loading" @select-example="useExample" />

    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>

    <ChatInput v-model="inputMessage" :loading="loading" @send="sendMessage" />

  </div>
</template>


<script setup lang="ts">
import ChatHeader
  from '@/components/chat/ChatHeader.vue'

import ChatMessageList
  from '@/components/chat/ChatMessageList.vue'

import ChatInput
  from '@/components/chat/ChatInput.vue'

import {
  useChat
} from '@/composables/useChat'


const {
  inputMessage,
  messages,
  loading,
  errorMessage,
  sendMessage,
  newConversation,
  useExample
} = useChat()
</script>


<style scoped>
.chat-view {
  height: calc(100vh - 64px);

  max-width: 1100px;

  margin: 0 auto;

  display: flex;
  flex-direction: column;
}


.error-message {
  margin: 8px 0;
  padding: 10px 14px;

  border-radius: 8px;

  background: #fff3f3;
  color: #c0392b;

  font-size: 14px;
}
</style>