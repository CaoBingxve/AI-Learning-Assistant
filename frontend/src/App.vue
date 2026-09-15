<template>
  <div class="App">
    <!-- <RouterLink to="/login">去Login</RouterLink><br> -->
    <RouterView></RouterView>

  </div>
</template>

<script setup lang="ts" name="App">
import { RouterLink, RouterView } from 'vue-router';
</script>

<style scoped></style>
