<template>

  <div class="home-view">

    <!-- =========================
         Header
    ========================== -->

    <section class="home-header">

      <div>

        <h1 class="page-title">

          欢迎回来，
          {{ username }}

          <span class="wave">
            👋
          </span>

        </h1>


        <p class="page-description">
          查看你的学习进度，继续今天的学习。
        </p>

      </div>


      <RouterLink :to="{ name: 'chat' }" class="primary-button copilot-button">
        ✦ 问 AI Copilot
      </RouterLink>

    </section>


    <!-- =========================
         Stats
    ========================== -->

    <HomeStats :total-records="records.length" :total-study-time="totalStudyTime" :total-study-hours="totalStudyHours"
      :latest-record="latestRecord" />


    <!-- =========================
         Quick Actions
    ========================== -->

    <QuickActions />


    <!-- =========================
         Recent Records
    ========================== -->

    <RecentRecords :records="recentRecords" :loading="loading" :error-message="errorMessage" @retry="loadRecords" />

  </div>

</template>


<script setup lang="ts">

import {
  computed,
  onMounted
} from 'vue'


import {
  useUserStore
} from '@/stores/user'


import {
  useRecords
} from '@/composables/useRecords'


import HomeStats
  from '@/components/home/HomeStats.vue'

import QuickActions
  from '@/components/home/QuickActions.vue'

import RecentRecords
  from '@/components/home/RecentRecords.vue'


/* =========================
   User
========================== */

const userStore =
  useUserStore()


const username =
  computed(() => {

    return (
      userStore.currentUser
        ?.username
      ??
      '学习者'
    )
  })


/* =========================
   Records
========================== */

const {

  records,

  sortedRecords,

  totalStudyTime,

  totalStudyHours,

  loading,

  errorMessage,

  loadRecords

} = useRecords()


/**
 * 最近一次学习
 */
const latestRecord =
  computed(() => {

    return (
      sortedRecords.value[0]
      ??
      null
    )
  })


/**
 * 首页只展示最近3条
 */
const recentRecords =
  computed(() => {

    return sortedRecords.value
      .slice(0, 3)
  })


/* =========================
   初始化
========================== */

onMounted(() => {

  loadRecords()

})

</script>


<style scoped>
.home-view {
  max-width: 1100px;

  margin: 0 auto;
}


/* =========================
   Header
========================== */

.home-header {
  display: flex;

  align-items: center;
  justify-content: space-between;

  gap: 24px;

  margin-bottom: 30px;
}


.wave {
  display: inline-block;

  margin-left: 4px;
}


.copilot-button {
  flex-shrink: 0;

  text-decoration: none;
}


@media (max-width: 700px) {

  .home-header {
    align-items: flex-start;

    flex-direction: column;
  }

}
</style>