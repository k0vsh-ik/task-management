<script setup>
import { reactive, ref, watch, computed } from 'vue';
import ConfirmEditModal from "@/components/ConfirmEditModal.vue";

// Props: optional task for editing and isEdit flag
const props = defineProps({
  task: Object,
  isEdit: Boolean
});

// Emits for save and close actions
const emit = defineEmits(['save', 'close']);

// Local copy of task to avoid modifying props directly
const localTask = reactive({
  title: '',
  description: '',
  status: 'To Do',
  created_at: null
});

// Populate localTask when props.task changes
watch(
    () => props.task,
    (newTask) => {
      if (newTask) {
        localTask.title = newTask.title;
        localTask.description = newTask.description;
        localTask.status = newTask.status;
        localTask.created_at = newTask.created_at || null;
      } else {
        localTask.title = '';
        localTask.description = '';
        localTask.status = 'To Do';
        localTask.created_at = null;
      }
    },
    { immediate: true }
);

// Show confirmation modal
const showEditConfirm = ref(false);

// Validate fields
const isValid = computed(() => {
  return localTask.title.trim() !== '' && localTask.description.trim() !== '';
});

// Trigger save confirmation
function handleSaveClick() {
  if (!isValid.value) return;
  showEditConfirm.value = true;
}

// Confirm save
function handleConfirmEdit() {
  saveTask();
  showEditConfirm.value = false;
}

// Cancel confirmation
function handleCancelEditConfirm() {
  showEditConfirm.value = false;
}

// Save task and emit event
function saveTask() {
  if (!localTask.created_at) {
    localTask.created_at = new Date().toISOString();
  }

  emit('save', { ...localTask });

  // Reset form fields
  localTask.title = '';
  localTask.description = '';
  localTask.status = 'To Do';
  localTask.created_at = null;
}
</script>

<template>
  <div class="fixed inset-0 bg-gray-500/50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg w-96 p-6 relative">
      <h3 class="text-lg font-semibold mb-4">
        {{ isEdit ? 'Edit Task' : 'Add New Task' }}
      </h3>

      <input
          v-model="localTask.title"
          type="text"
          placeholder="Title"
          :class="[
          'w-full px-3 py-2 border rounded mb-3 focus:outline-none focus:ring-2',
          localTask.title.trim() ? 'focus:ring-blue-400 border-gray-300' : 'border-red-500 focus:ring-red-400'
        ]"
      />

      <textarea
          v-model="localTask.description"
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
        <button @click="$emit('close')" class="px-4 py-2 rounded border hover:bg-gray-100">Cancel</button>

        <button
            @click="handleSaveClick"
            :class="[
            'px-4 py-2 rounded text-white',
            isValid ? 'bg-blue-600 hover:bg-blue-700' : 'bg-gray-400 cursor-not-allowed'
          ]"
        >
          {{ isEdit ? 'Save' : 'Add' }}
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
