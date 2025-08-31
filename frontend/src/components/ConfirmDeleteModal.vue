<script setup lang="ts">
defineProps<{
  show: boolean;
  message: string;
}>();

const emit = defineEmits<{
  (e: 'confirm'): void;
  (e: 'cancel'): void;
}>();

function handleConfirm() {
  emit('confirm');
}

function handleCancel() {
  emit('cancel');
}
</script>

<template>
  <div
      v-if="show"
      class="fixed inset-0 bg-gray-500/50 flex items-center justify-center z-50"
  >
    <div class="bg-white rounded-lg shadow-lg p-6 w-80">
      <h3 class="text-lg font-semibold mb-4">Confirm Action</h3>
      <p class="mb-6">{{ message }}</p>
      <div class="flex justify-end gap-3">
        <button
            name="cancelDeleteButton"
            @click="handleCancel"
            class="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400"
        >
          Cancel
        </button>
        <button
            name="confirmDeleteButton"
            @click="handleConfirm"
            class="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
        >
          Delete
        </button>
      </div>
    </div>
  </div>
</template>
