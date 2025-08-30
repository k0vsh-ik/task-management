<script setup lang="ts">
import { reactive, ref, watch, computed } from 'vue';
import ConfirmEditModal from "@/components/ConfirmEditModal.vue";
import type { TaskItem } from "@/types/models";

// Props
const props = defineProps<{
  task?: TaskItem | null;
  isEdit: boolean;
}>();

// Emits
const emit = defineEmits<{
  (e: 'save', task: TaskItem): void;
  (e: 'close'): void;
}>();

// Local task
const localTask = reactive<TaskItem>({
  id: props.task?.id ?? 0,
  title: props.task?.title ?? '',
  description: props.task?.description ?? '',
  status: props.task?.status ?? 'To Do',
  created_at: props.task?.created_at ?? new Date().toISOString(),
});

// Watch task prop
watch(
    () => props.task,
    (newTask) => {
      if (newTask) {
        Object.assign(localTask, newTask);
      } else {
        localTask.id = 0;
        localTask.title = '';
        localTask.description = '';
        localTask.status = 'To Do';
        localTask.created_at = new Date().toISOString();
      }
    },
    { immediate: true }
);

function resetLocalTask() {
  localTask.id = 0;
  localTask.title = '';
  localTask.description = '';
  localTask.status = 'To Do';
  localTask.created_at = new Date().toISOString();
}

function handleClose() {
  resetLocalTask();
  emit('close');
}


// Confirmation
const showEditConfirm = ref(false);
const isValid = computed(() => localTask.title.trim() !== '' && localTask.description.trim() !== '');

function handleSaveClick() {
  if (!isValid.value) return;
  showEditConfirm.value = true;
}

function handleConfirmEdit() {
  saveTask();
  showEditConfirm.value = false;
}

function handleCancelEditConfirm() {
  showEditConfirm.value = false;
}

function saveTask() {
  if (!localTask.created_at) localTask.created_at = new Date().toISOString();

  emit('save', { ...localTask });
  if (!props.isEdit) resetLocalTask();


  // Reset only if adding
  if (!props.isEdit) {
    localTask.id = 0;
    localTask.title = '';
    localTask.description = '';
    localTask.status = 'To Do';
    localTask.created_at = new Date().toISOString();
  }
}
</script>

<template>
  <div class="fixed inset-0 bg-gray-500/50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg w-96 p-6 relative">
      <h3 class="text-lg font-semibold mb-4">
        {{ props.isEdit ? 'Edit Task' : 'Add New Task' }}
      </h3>

      <input
          v-model="localTask.title"
          name="title"
          type="text"
          placeholder="Title"
          :class="[
        'w-full px-3 py-2 border rounded mb-3 focus:outline-none focus:ring-2',
        localTask.title.trim() ? 'focus:ring-blue-400 border-gray-300' : 'border-red-500 focus:ring-red-400'
      ]"
      />

      <textarea
          v-model="localTask.description"
          name="description"
          placeholder="Description"
          :class="[
        'w-full px-3 py-2 border rounded mb-3 focus:outline-none focus:ring-2',
        localTask.description.trim() ? 'focus:ring-blue-400 border-gray-300' : 'border-red-500 focus:ring-red-400'
      ]"
      ></textarea>

      <select
          v-model="localTask.status"
          class="w-full px-3 py-2 border rounded mb-4 focus:outline-none focus:ring-2 focus:ring-blue-400"
      >
        <option>To Do</option>
        <option>In Progress</option>
        <option>Done</option>
      </select>

      <div class="flex justify-end space-x-2">
        <button name="cancelbtn" @click="handleClose" class="px-4 py-2 rounded border hover:bg-gray-100">Cancel</button>

        <button
            name="savebtn"
            @click="handleSaveClick"
            :class="[
          'px-4 py-2 rounded text-white',
          isValid ? 'bg-blue-600 hover:bg-blue-700' : 'bg-gray-400 cursor-not-allowed'
        ]"
        >
          {{ props.isEdit ? 'Save' : 'Add' }}
        </button>

        <ConfirmEditModal
            :show="showEditConfirm"
            message="Are you sure you want to save changes?"
            @confirm="handleConfirmEdit"
            @cancel="handleCancelEditConfirm"
        />
      </div>
    </div>
  </div>
</template>
