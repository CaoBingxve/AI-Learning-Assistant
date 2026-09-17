<template>

  <div class="chat-page">

    <!-- 左侧历史会话 -->
    <ChatHistory :conversations="conversations
      " :active-conversation-id="activeConversationId
        " @new-chat="
        newConversation
      " @select="
        selectConversation
      " />


    <!-- 右侧聊天主体 -->
    <div class="chat-main">

      <ChatHeader @new-chat="
        newConversation
      " />


      <ChatMessageList :messages="messages
        " :loading="loading
          " @select-example="
          useExample
        " />


      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>


      <ChatInput v-model="inputMessage
        " :loading="loading
          " @send="
          sendMessage
        " />

    </div>

  </div>

</template>


<script setup lang="ts">

import {
  onMounted
} from 'vue'


import ChatHeader
  from '@/components/chat/ChatHeader.vue'

import ChatHistory
  from '@/components/chat/ChatHistory.vue'

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

  conversations,

  activeConversationId,

  loading,

  errorMessage,

  initializeChat,

  sendMessage,

  newConversation,

  selectConversation,

  useExample

} = useChat()


onMounted(() => {

  initializeChat()

})

</script>


<style scoped>
.chat-page {
  height:
    calc(100vh - 48px);

  display: flex;

  overflow: hidden;

  border:
    1px solid var(--color-border);

  border-radius:
    var(--radius-medium);

  background:
    var(--color-surface);

  box-shadow:
    var(--shadow-card);
}


.chat-main {
  min-width: 0;

  flex: 1;

  display: flex;

  flex-direction: column;
}


.error-message {
  margin:
    0 20px 10px;

  padding:
    10px 13px;

  border-radius: 8px;

  background: #fff3f3;

  color:
    var(--color-danger);

  font-size: 13px;
}
</style>