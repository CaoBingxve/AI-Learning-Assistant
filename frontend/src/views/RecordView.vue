<template>
  <div class="recordView">
    <h2>学习记录</h2>

    <!-- 添加模式 -->
    <div class="addRecord" v-if="add">
      <div>
        <label>标题：</label>
        <input v-model="title" type="text" placeholder="请输入标题" />
      </div>
      <div>
        <label>内容：</label>
        <textarea v-model="content" placeholder="请输入内容"></textarea>
      </div>
      <div>
        <label>学习时间：</label>
        <input v-model.number="studyTime" type="number" min="1" placeholder="请输入学习时间" />
      </div>
      <button @click="handleCreateRecord" :disabled="creating">
        {{ creating ? '添加中...' : '确认添加' }}
      </button>
    </div>

    <!-- 列表模式 -->
    <div v-else>
      <div v-if="loading">
        加载中……
      </div>
      <div v-else>
        <div v-for="record in records" :key="record.id" class="record-item">
          <h4>{{ record.title }}</h4>
          <p>{{ record.content }}</p>
          <p>学习时长：{{ record.study_time }}分钟</p>
          <p>创建时间：{{ formatDate(record.created_at) }}</p>
        </div>
        <p v-if="records.length === 0">
          暂无学习记录
        </p>
      </div>
    </div>
    <button @click="add = !add">
      {{ add ? '取消添加' : '添加记录' }}
    </button>
    <p v-if="errorMessage" style="color: red">
      {{ errorMessage }}
    </p>

  </div>
</template>

<script setup lang="ts" name="recordView">
import { createRecordApi, getRecordsApi } from '@/api/record';
import { onMounted, ref } from 'vue';
import type { RecordResponse } from '@/api/record';

// 数据
const title = ref('')
const content = ref('')
const studyTime = ref(0)
const errorMessage = ref('')
const add = ref(false)
const loading = ref(true)
const creating = ref(false)
// TS加上泛型
const records = ref<RecordResponse[]>([])

// 刷新列表函数，抽出来，初始化、新增完成都调用
async function refreshRecordList() {
  loading.value = true
  errorMessage.value = ''
  try {
    const res = await getRecordsApi()
    records.value = res.data
  } catch (e) {
    errorMessage.value = "获取列表失败"
  } finally {
    loading.value = false
  }
}

async function handleCreateRecord() {
  errorMessage.value = ''

  if (!title.value.trim() || !content.value.trim() || studyTime.value <= 0) {
    errorMessage.value = '请填写所有信息，学习时间必须大于0'
    return
  }
  // 防止重复点击
  if (creating.value) return
  creating.value = true

  console.log('创建记录:', {
    title: title.value,
    content: content.value,
    studyTime: studyTime.value,
  })

  try {
    await createRecordApi({
      title: title.value,
      content: content.value,
      study_time: studyTime.value
    })
    // 清空表单
    title.value = ''
    content.value = ''
    studyTime.value = 0
    add.value = false
    // 新增完成重新拉取列表，页面立刻刷新
    await refreshRecordList()
  } catch (error) {
    errorMessage.value = '创建失败'
  } finally {
    creating.value = false
  }
}

// 页面挂载获取数据
onMounted(async () => {
  await refreshRecordList()
})

// 修改时间样式
function formatDate(date: string) {
  return new Date(date).toLocaleString()
}
</script>

<style scoped>
.record-item {
  border: 1px solid #ccc;
  padding: 12px;
  margin: 8px 0;
  border-radius: 6px;
}

.addRecord>div {
  margin: 8px 0;
}

label {
  display: inline-block;
  width: 80px;
}

input {
  padding: 4px;
}
</style>