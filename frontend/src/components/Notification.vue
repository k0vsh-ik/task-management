<script setup lang="ts">
defineProps<{
  message: string | null;
  isError: boolean;
}>();
</script>

<template>
  <transition name="fade">
    <div v-if="message" :class="['notification', isError ? 'error' : 'success']">
      {{ message }}
    </div>
  </transition>
</template>

<style scoped>
.notification {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 12px 18px;
  border-radius: 6px;
  color: #fff;
  font-weight: 600;
  z-index: 999;
}
.notification.success {
  background-color: #28a745;
}
.notification.error {
  background-color: #dc3545;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.4s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
