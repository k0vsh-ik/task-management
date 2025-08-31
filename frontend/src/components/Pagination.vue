<script setup lang="ts">
import {computed} from "vue";

const { currentPage, totalPages } = defineProps<{
  currentPage: number;
  totalPages: number;
}>();

const emit = defineEmits<(e: 'changePage', page: number) => void>();

const pagesToShow = computed(() => {
  const pages: (number | string)[] = [];

  if (totalPages <= 5) {
    for (let i = 1; i <= totalPages; i++) pages.push(i);
  } else {
    pages.push(1);

    if (currentPage > 3) pages.push('...');

    for (
        let i = Math.max(2, currentPage - 1);
        i <= Math.min(totalPages - 1, currentPage + 1);
        i++
    ) {
      pages.push(i);
    }

    if (currentPage < totalPages - 2) pages.push('...');
    pages.push(totalPages);
  }

  return pages;
});

function goToPage(page: number | string) {
  if (typeof page === 'number') emit('changePage', page);
}
</script>

<template>
  <div class="flex justify-center mt-4 space-x-2">
    <button
        v-for="page in pagesToShow"
        :key="page"
        @click="goToPage(page)"
        :class="[
        'px-3 py-1 rounded border transition',
        page === currentPage
          ? 'bg-blue-600 text-white border-blue-600'
          : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-100',
        page === '...' ? 'cursor-default' : ''
      ]"
        :disabled="page === '...'"
    >
      {{ page }}
    </button>
  </div>
</template>
