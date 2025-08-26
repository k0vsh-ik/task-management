<script setup>
import { computed } from 'vue';

// Define props
const props = defineProps({
  task: {
    type: Object,
    required: true
  }
});

// Compute CSS classes based on task status
const statusClasses = computed(() => {
  switch (props.task.status) {
    case 'Done':
      return 'bg-green-100 text-green-700';
    case 'In Progress':
      return 'bg-yellow-100 text-yellow-700';
    case 'To Do':
      return 'bg-gray-100 text-gray-700';
    default:
      return 'bg-gray-100 text-gray-700';
  }
});

// Format task creation date for display
const formattedDate = computed(() => {
  const date = new Date(props.task.created_at);
  return date.toLocaleString(undefined, { // uses user's local timezone
    year: 'numeric',
    month: 'short',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false
  });
});
</script>

<template>
  <tr class="hover:bg-gray-50 transition">
    <td class="px-4 py-2">{{ task.id }}</td>
    <td class="px-4 py-2">{{ task.title }}</td>
    <td class="px-4 py-2">{{ task.description }}</td>
    <td class="px-4 py-2">
      <span
          class="inline-block px-2 py-1 text-sm font-medium rounded-full"
          :class="statusClasses"
      >
        {{ task.status }}
      </span>
    </td>
    <td class="px-4 py-2">{{ formattedDate }}</td>
    <td class="px-4 py-2">
      <div class="flex justify-end space-x-2">
        <button
            @click="$emit('edit', task)"
            class="text-blue-600 hover:text-blue-800 px-2 py-1 rounded pi pi-pencil"
        ></button>
        <button
            @click="$emit('delete', task.id)"
            class="text-red-600 hover:text-red-800 px-2 py-1 rounded pi pi-trash"
        ></button>
      </div>
    </td>
  </tr>
</template>
