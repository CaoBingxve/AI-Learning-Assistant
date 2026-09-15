<template>

  <div class="record-view">

    <!-- 页面标题 -->
    <section class="page-header">

      <div>

        <h1 class="page-title">
          学习记录
        </h1>

        <p class="page-description">
          记录每天学了什么，让 Copilot 更了解你的学习情况。
        </p>

      </div>


      <button class="primary-button add-button" @click="toggleAddMode">

        {{
          addMode
            ? '取消添加'
            : '+ 新增记录'
        }}

      </button>

    </section>


    <!-- 统计 -->
    <RecordStats :total-records="records.length" :total-study-time="totalStudyTime" :total-study-hours="totalStudyHours"
      :average-study-time="averageStudyTime" />


    <!-- 新增模式 -->
    <RecordForm v-if="addMode" :creating="creating" :error-message="createError" @submit="handleCreateRecord"
      @cancel="cancelCreate" />


    <!-- 列表模式 -->
    <RecordList v-else :records="sortedRecords" :loading="loading" :error-message="errorMessage" @retry="loadRecords"
      @add="openCreateMode" />

  </div>

</template>


<script setup lang="ts">

import {
  onMounted,
  ref
} from 'vue'

import {
  createRecordApi
} from '@/api/record'

import type {
  RecordCreate
} from '@/api/record'

import {
  useRecords
} from '@/composables/useRecords'

import RecordStats
  from '@/components/record/RecordStats.vue'

import RecordForm
  from '@/components/record/RecordForm.vue'

import RecordList
  from '@/components/record/RecordList.vue'


/* =========================
   学习记录数据
========================= */

const {

  records,

  sortedRecords,

  totalStudyTime,

  totalStudyHours,

  averageStudyTime,

  loading,

  errorMessage,

  loadRecords

} = useRecords()


/* =========================
   页面状态
========================= */

const addMode =
  ref(false)

const creating =
  ref(false)

const createError =
  ref('')


/* =========================
   创建记录
========================= */

async function handleCreateRecord(
  data: RecordCreate
) {

  if (creating.value) {
    return
  }


  createError.value = ''

  creating.value = true


  try {

    await createRecordApi(
      data
    )


    /*
     * 创建成功后：
     *
     * 1. 退出新增模式
     * 2. 重新获取列表
     */
    addMode.value = false


    await loadRecords()


  } catch (error) {

    console.error(
      '创建学习记录失败：',
      error
    )


    createError.value =
      '学习记录保存失败，请稍后重试。'


  } finally {

    creating.value = false
  }
}


/* =========================
   页面交互
========================= */

function openCreateMode() {

  createError.value = ''

  addMode.value = true
}


function cancelCreate() {

  createError.value = ''

  addMode.value = false
}


function toggleAddMode() {

  createError.value = ''

  addMode.value =
    !addMode.value
}


/* =========================
   初始化
========================= */

onMounted(() => {

  loadRecords()

})

</script>


<style scoped>
.record-view {
  max-width: 1100px;

  margin: 0 auto;
}


.page-header {
  display: flex;

  align-items: center;
  justify-content: space-between;

  gap: 20px;

  margin-bottom: 28px;
}


.add-button {
  flex-shrink: 0;
}


@media (max-width: 800px) {

  .page-header {
    align-items: flex-start;

    flex-direction: column;
  }

}
</style>