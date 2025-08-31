<script setup lang="ts">
import { computed } from 'vue';

const { task } = defineProps<{
  task: {
    id: number;
    title: string;
    description: string;
    status: string;
    created_at: string;
  };
}>();

const statusClasses = computed(() => {
  const statusMap: Record<string, string> = {
    'Done': 'bg-green-100 text-green-700',
    'In Progress': 'bg-yellow-100 text-yellow-700',
    'To Do': 'bg-gray-100 text-gray-700',
  };
  return statusMap[task.status] ?? 'bg-gray-100 text-gray-700';
});

const formattedDate = computed(() => {
  const date = new Date(task.created_at);
  return date.toLocaleString(undefined, {
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
      <span class="inline-block px-2 py-1 text-sm font-medium rounded-full" :class="statusClasses">
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
