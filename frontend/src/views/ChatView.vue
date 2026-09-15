<template>
  <div class="chatView">
    <h2>AI 学习助手</h2>
    <!-- 聊天信息 -->
    <div class="message-list">
      <div v-for="(message, index) in messages" :key="index" class="message">
        <strong>
          {{ message.role === 'user' ? '你' : 'AI' }}:
        </strong>

        <span>{{ message.content }}</span>
      </div>
      <p v-if="loading">AI正在思考...</p>
      <p v-if="messages?.length === 0">还没有对话，问我一个问题吧。</p>
    </div>

    <!-- 错误提示 -->
    <p v-if="errorMessage" class="error">
      {{ errorMessage }}
    </p>

    <!-- 输入区域 -->
    <div class="input-area">
      <textarea v-model="inputMessage" placeholder="请输入你的问题">
    </textarea>
      <button @click="sendMessage" :disabled="loading">{{ loading ? '回答中...' : '发送' }}</button>
    </div>
  </div>
</template>

<script setup lang="ts" name="chatView">
import { ref } from 'vue';
import { copilotApi, ChatMessage } from '@/api/chat';

const inputMessage = ref('')

const messages = ref<ChatMessage[]>([])

const loading = ref(false)

const errorMessage = ref('')

async function sendMessage() {
  errorMessage.value = ''

  const message = inputMessage.value.trim()

  if (!message) {
    return
  }
  if (loading.value) {
    return
  }

  messages.value.push({
    role: 'user',
    content: message
  })

  inputMessage.value = ''
  loading.value = true

  try {
    const response = await copilotApi({
      message
    })

    messages.value.push({
      role: "assistant",
      content: response.data.answer
    })
  } catch {
    errorMessage.value = 'AI回答失败，请稍后重试'

  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.chat-view {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}


.message-list {
  min-height: 400px;
  margin-bottom: 20px;
}


.message {
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #ddd;
  border-radius: 6px;
}


.input-area {
  display: flex;
  gap: 10px;
}


textarea {
  flex: 1;
  min-height: 80px;
  padding: 8px;
}


button {
  padding: 8px 16px;
}


.error {
  color: red;
}
</style>