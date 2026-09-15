<template>
  <div class="chat-view">

    <!-- 顶部标题 -->
    <div class="chat-header">
      <div>
        <h2>AI Learning Copilot</h2>
        <p>结合你的学习记录和知识库，为你提供学习建议</p>
      </div>
      <button class="new-chat-button" @click="newConversation">
        新对话
      </button>
    </div>


    <!-- 聊天区域 -->
    <div ref="messageListRef" class="message-list">

      <!-- 空状态 -->
      <div v-if="messages.length === 0 && !loading" class="empty-state">
        <h3>今天想学点什么？</h3>

        <p>
          你可以让我查询知识库、
          分析学习记录，或者直接问一个学习问题。
        </p>

        <div class="example-list">
          <button class="example-item" @click="useExample('给我看看我的学习记录')">
            给我看看我的学习记录
          </button>

          <button class="example-item" @click="useExample('根据我最近的学习记录，分析我接下来最值得复习什么')">
            帮我分析下一步该复习什么
          </button>

          <button class="example-item" @click="useExample('Copilot的内部测试代号是什么？')">
            查询知识库内容
          </button>
        </div>
      </div>


      <!-- 消息列表 -->
      <div v-for="(message, index) in messages" :key="index" class="message-row" :class="message.role">
        <div class="message-wrapper">

          <div class="message-name">
            {{
              message.role === 'user'
                ? '你'
                : 'AI Copilot'
            }}
          </div>

          <div class="message-bubble message-content" v-html="renderMarkdown(message.content)"></div>

        </div>
      </div>


      <!-- AI loading -->
      <div v-if="loading" class="message-row assistant">
        <div class="message-wrapper">

          <div class="message-name">
            AI Copilot
          </div>

          <div class="message-bubble loading-message">
            <span class="loading-dot"></span>
            <span class="loading-dot"></span>
            <span class="loading-dot"></span>

            <span class="loading-text">
              正在分析你的问题...
            </span>
          </div>

        </div>
      </div>

    </div>


    <!-- 错误提示 -->
    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>


    <!-- 输入区域 -->
    <div class="input-area">

      <textarea v-model="inputMessage" placeholder="问 Copilot 一个学习问题..." :disabled="loading"
        @keydown.enter.exact.prevent="sendMessage"></textarea>

      <button class="send-button" @click="sendMessage" :disabled="loading || !inputMessage.trim()">
        {{ loading ? '思考中...' : '发送' }}
      </button>

    </div>


    <div class="input-tip">
      Enter 发送 · Shift + Enter 换行
    </div>

  </div>
</template>


<script setup lang="ts">
const CONVERSATION_KEY =
  'copilot_conversation_id'


function getConversationId() {

  let id = localStorage.getItem(
    CONVERSATION_KEY
  )

  if (!id) {

    id = crypto.randomUUID()

    localStorage.setItem(
      CONVERSATION_KEY,
      id
    )
  }

  return id
}


const conversationId =
  ref(getConversationId())

import {
  nextTick,
  ref
} from 'vue'

import { marked } from 'marked'
import DOMPurify from 'dompurify'

import {
  copilotApi,
  type ChatMessage
} from '@/api/chat'


const inputMessage = ref('')

const messages = ref<ChatMessage[]>([])

const loading = ref(false)

const errorMessage = ref('')

const messageListRef =
  ref<HTMLElement | null>(null)


/**
 * Markdown → HTML
 * 再经过 DOMPurify 清理，避免直接插入不安全 HTML
 */
function renderMarkdown(content: string) {
  const html = marked.parse(
    content,
    {
      async: false
    }
  ) as string

  return DOMPurify.sanitize(html)
}


/**
 * 滚动到聊天区域最底部
 */
async function scrollToBottom() {
  await nextTick()

  if (!messageListRef.value) {
    return
  }

  messageListRef.value.scrollTop =
    messageListRef.value.scrollHeight
}


/**
 * 点击示例问题
 */
function useExample(message: string) {
  inputMessage.value = message
}


/**
 * 发送消息
 */
async function sendMessage() {

  errorMessage.value = ''

  const message =
    inputMessage.value.trim()


  // 空内容不发送
  if (!message) {
    return
  }


  // AI 正在回答时不重复发送
  if (loading.value) {
    return
  }


  // 先显示用户消息
  messages.value.push({
    role: 'user',
    content: message
  })


  // 清空输入框
  inputMessage.value = ''


  // 显示 loading
  loading.value = true


  // 用户消息加入后自动滚到底部
  await scrollToBottom()


  try {

    // 调用 Learning Copilot
    const response = await copilotApi({
      message,
      conversation_id: conversationId.value
    })


    // 添加 AI 回答
    messages.value.push({
      role: 'assistant',
      content: response.data.answer
    })


    // AI回答完成后滚动到底部
    await scrollToBottom()

  } catch (error) {

    console.error(
      'Copilot调用失败：',
      error
    )

    errorMessage.value =
      'AI Copilot 暂时无法回答，请稍后重试。'

  } finally {

    loading.value = false

    await scrollToBottom()
  }
}
function newConversation() {

  const id = crypto.randomUUID()

  conversationId.value = id

  localStorage.setItem(
    CONVERSATION_KEY,
    id
  )

  messages.value = []

  errorMessage.value = ''
}
</script>


<style scoped>
/* ==============================
   页面整体
============================== */

.chat-view {
  height: calc(100vh - 40px);
  max-width: 1000px;

  margin: 0 auto;
  padding: 20px 24px;

  box-sizing: border-box;

  display: flex;
  flex-direction: column;
}


/* ==============================
   Header
============================== */

.chat-header {
  padding-bottom: 16px;

  border-bottom: 1px solid #eeeeee;
}

.chat-header h2 {
  margin: 0;

  font-size: 24px;
  font-weight: 600;
}

.chat-header p {
  margin: 6px 0 0;

  font-size: 14px;
  color: #777777;
}


/* ==============================
   聊天列表
============================== */

.message-list {
  flex: 1;

  overflow-y: auto;

  padding: 24px 8px;

  scroll-behavior: smooth;
}


/* ==============================
   空状态
============================== */

.empty-state {
  max-width: 600px;

  margin: 90px auto 0;

  text-align: center;
}

.empty-state h3 {
  margin-bottom: 10px;

  font-size: 25px;
}

.empty-state p {
  margin-bottom: 28px;

  color: #777777;
  line-height: 1.7;
}


.example-list {
  display: flex;
  flex-direction: column;

  gap: 10px;
}


.example-item {
  padding: 13px 16px;

  background: #ffffff;

  border: 1px solid #dddddd;
  border-radius: 10px;

  cursor: pointer;

  font-size: 14px;

  transition: 0.2s;
}


.example-item:hover {
  background: #f7f7f7;

  transform: translateY(-1px);
}


/* ==============================
   消息
============================== */

.message-row {
  display: flex;

  margin-bottom: 22px;
}


/* 用户靠右 */
.message-row.user {
  justify-content: flex-end;
}


/* AI靠左 */
.message-row.assistant {
  justify-content: flex-start;
}


.message-wrapper {
  max-width: 78%;
}


/* 用户名称 */
.message-name {
  margin-bottom: 6px;

  font-size: 13px;
  color: #777777;
}


.user .message-name {
  text-align: right;
}


.message-bubble {
  padding: 14px 18px;

  border-radius: 14px;

  line-height: 1.75;

  word-break: break-word;
}


/* 用户消息 */
.user .message-bubble {
  background: #f1f1f1;
}


/* AI消息 */
.assistant .message-bubble {
  background: #ffffff;

  border: 1px solid #e5e5e5;
}


/* ==============================
   Markdown 内容
============================== */

.message-content :deep(p) {
  margin: 8px 0;
}


.message-content :deep(h1) {
  margin: 8px 0 14px;

  font-size: 22px;
}


.message-content :deep(h2) {
  margin: 18px 0 10px;

  font-size: 19px;
}


.message-content :deep(h3) {
  margin: 16px 0 8px;

  font-size: 17px;
}


.message-content :deep(ul),
.message-content :deep(ol) {
  margin: 8px 0;

  padding-left: 24px;
}


.message-content :deep(li) {
  margin: 5px 0;
}


.message-content :deep(strong) {
  font-weight: 600;
}


.message-content :deep(blockquote) {
  margin: 12px 0;

  padding: 8px 14px;

  border-left: 4px solid #dddddd;

  background: #f8f8f8;
}


.message-content :deep(code) {
  padding: 2px 6px;

  background: #f4f4f4;

  border-radius: 4px;

  font-family:
    Consolas,
    Monaco,
    monospace;

  font-size: 13px;
}


.message-content :deep(pre) {
  overflow-x: auto;

  margin: 12px 0;

  padding: 14px;

  background: #f5f5f5;

  border-radius: 8px;
}


.message-content :deep(pre code) {
  padding: 0;

  background: transparent;
}


/* Markdown 表格 */
.message-content :deep(table) {
  width: 100%;

  margin: 14px 0;

  border-collapse: collapse;
}


.message-content :deep(th),
.message-content :deep(td) {
  padding: 8px 10px;

  border: 1px solid #dddddd;

  text-align: left;
}


.message-content :deep(th) {
  background: #f7f7f7;
}


/* ==============================
   Loading
============================== */

.loading-message {
  display: flex;

  align-items: center;

  gap: 5px;

  color: #666666;
}


.loading-dot {
  width: 6px;
  height: 6px;

  border-radius: 50%;

  background: #999999;

  animation: loading-bounce 1.4s infinite ease-in-out;
}


.loading-dot:nth-child(2) {
  animation-delay: 0.15s;
}


.loading-dot:nth-child(3) {
  animation-delay: 0.3s;
}


.loading-text {
  margin-left: 6px;
}


@keyframes loading-bounce {

  0%,
  60%,
  100% {
    transform: translateY(0);
    opacity: 0.5;
  }

  30% {
    transform: translateY(-4px);
    opacity: 1;
  }
}


/* ==============================
   Error
============================== */

.error-message {
  margin: 8px 0;

  padding: 10px 14px;

  border-radius: 8px;

  background: #fff3f3;

  color: #c0392b;

  font-size: 14px;
}


/* ==============================
   输入区域
============================== */

.input-area {
  display: flex;

  align-items: flex-end;

  gap: 12px;

  padding-top: 16px;

  border-top: 1px solid #eeeeee;
}


.input-area textarea {
  flex: 1;

  min-height: 52px;
  max-height: 140px;

  resize: vertical;

  padding: 12px 14px;

  box-sizing: border-box;

  border: 1px solid #dddddd;
  border-radius: 10px;

  outline: none;

  font-family: inherit;
  font-size: 15px;

  line-height: 1.5;

  transition: border-color 0.2s;
}


.input-area textarea:focus {
  border-color: #999999;
}


.input-area textarea:disabled {
  background: #f8f8f8;
}


.send-button {
  height: 46px;

  padding: 0 22px;

  border: none;
  border-radius: 10px;

  cursor: pointer;

  font-size: 14px;
  font-weight: 500;

  background: #222222;
  color: #ffffff;

  transition: 0.2s;
}


.send-button:hover:not(:disabled) {
  opacity: 0.85;
}


.send-button:disabled {
  cursor: not-allowed;

  opacity: 0.45;
}


.input-tip {
  padding-top: 7px;

  text-align: center;

  font-size: 12px;
  color: #999999;
}


/* ==============================
   滚动条
============================== */

.message-list::-webkit-scrollbar {
  width: 6px;
}


.message-list::-webkit-scrollbar-thumb {
  background: #d5d5d5;

  border-radius: 10px;
}


/* ==============================
   小屏幕
============================== */

@media (max-width: 768px) {

  .chat-view {
    padding: 14px;
  }

  .message-wrapper {
    max-width: 90%;
  }

  .input-area {
    gap: 8px;
  }

  .send-button {
    padding: 0 16px;
  }
}
</style>