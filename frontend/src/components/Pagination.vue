<script setup>

// Define component props
const props = defineProps({
  currentPage: Number,
  totalPages: Number,
});

// Define component emits
const emits = defineEmits(['changePage']);

// Compute pages to display in pagination
function pagesToShow() {
  const pages = [];

  if (props.totalPages <= 5) {
    for (let i = 1; i <= props.totalPages; i++) pages.push(i);
  } else {
    pages.push(1);

    if (props.currentPage > 3) pages.push('...');

    for (
        let i = Math.max(2, props.currentPage - 1);
        i <= Math.min(props.totalPages - 1, props.currentPage + 1);
        i++
    ) {
      pages.push(i);
    }

    if (props.currentPage < props.totalPages - 2) pages.push('...');
    pages.push(props.totalPages);
  }

  return pages;
}

// Emit page change
function goToPage(page) {
  if (page !== '...') {
    emits('changePage', page);
  }
}
</script>

<template>
  <div class="flex justify-center mt-4 space-x-2">
    <button
        v-for="page in pagesToShow()"
        :key="page + Math.random()"
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
