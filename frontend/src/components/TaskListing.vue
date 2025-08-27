<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue';
import { useTasks } from '@/composables/useTasks.js';
import ConfirmDeleteModal from "@/components/ConfirmDeleteModal.vue";
import DownloadCSV from "@/components/DownloadCSV.vue";
import type {TaskItem} from "@/types/models";
import Task from "@/components/Task.vue";
import Pagination from "@/components/Pagination.vue";
import TaskModal from "@/components/TaskModal.vue";

// Tasks composable
const { tasks, totalTasks, fetchTasks, deleteTask, saveTask } = useTasks();

// Pagination state
const currentPage = ref(1);
const pageSize = ref(10);
const totalPages = computed(() => Math.ceil(totalTasks.value / pageSize.value));

// Modal and editing state
const showModal = ref(false);
const isEditing = ref(false);
const editingTask = ref<TaskItem | null>(null);

// Status filter
const statusFilter = ref<string | null>(null);
const statusOptions = ["To Do", "In Progress", "Done"];

// Open add task modal
function openAddModal() {
  isEditing.value = false;
  editingTask.value = null;
  showModal.value = true;
}

// Open edit task modal
function openEditModal(task: TaskItem) {
  isEditing.value = true;
  editingTask.value = task;
  showModal.value = true;
}

// Save task handler
async function handleSave(newTaskData: TaskItem) {
  await saveTask(newTaskData, isEditing.value, editingTask.value?.id);
  await fetchTasks(currentPage.value, pageSize.value);
  showModal.value = false;
}

// Delete task handler
async function handleDelete(taskId: number) {
  await deleteTask(taskId);
  await fetchTasks(currentPage.value, pageSize.value);
}

// Handle page change
function onPageChange(page: number) {
  currentPage.value = page;
  fetchTasks(page, pageSize.value, statusFilter.value);
}

// Delete confirmation modal state
const showDeleteModal = ref(false);
const taskToDelete = ref<number | null>(null);

function confirmDelete(taskId: number) {
  taskToDelete.value = taskId;
  showDeleteModal.value = true;
}

async function handleDeleteConfirm() {
  if (taskToDelete.value !== null) {
    await deleteTask(taskToDelete.value);
    await fetchTasks(currentPage.value, pageSize.value);
    taskToDelete.value = null;
    showDeleteModal.value = false;
  }
}

function handleDeleteCancel() {
  taskToDelete.value = null;
  showDeleteModal.value = false;
}

// Watch for status filter changes
watch(statusFilter, () => {
  currentPage.value = 1; // reset page
  fetchTasks(currentPage.value, pageSize.value, statusFilter.value);
});

// Fetch tasks on mount
onMounted(() => fetchTasks(currentPage.value, pageSize.value, statusFilter.value));
</script>

<template>
  <div class="min-h-screen bg-gray-100 flex flex-col items-center">
    <main class="w-full max-w-5xl mt-10 p-6 bg-white rounded-lg shadow-lg">
      <!-- Header -->
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold text-gray-700">Your Tasks</h2>
        <button
            @click="openAddModal"
            class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
        >
          + Add Task
        </button>
      </div>

      <!-- Tasks table -->
      <div class="overflow-x-auto">
        <table class="min-w-full border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-100">
          <tr>
            <th class="px-4 py-2 text-left text-gray-700 font-semibold">ID</th>
            <th class="px-4 py-2 text-left text-gray-700 font-semibold">Title</th>
            <th class="px-4 py-2 text-left text-gray-700 font-semibold">Description</th>
            <th class="px-4 py-2 text-left text-gray-700 font-semibold">
              <select v-model="statusFilter">
                <option :value="null">Status</option>
                <option
                    v-for="status in statusOptions"
                    :key="status"
                    :value="status"
                >
                  {{ status }}
                </option>
              </select>
            </th>
            <th class="px-4 py-2 text-left text-gray-700 font-semibold">Created Date</th>
            <th class="px-4 py-2 text-right text-gray-700 font-semibold">Actions</th>
          </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
          <Task
              v-for="task in tasks"
              :key="task.id"
              :task="task"
              @edit="openEditModal"
              @delete="confirmDelete(task.id)"
          />
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <Pagination
          :currentPage="currentPage"
          :totalPages="totalPages"
          @changePage="onPageChange"
      />

      <div class="text-center mt-2 text-gray-600">
        Total Tasks: {{ totalTasks }}
      </div>

      <!-- Task modal -->
      <TaskModal
          v-if="showModal"
          :task="editingTask"
          :isEdit="isEditing"
          @save="handleSave"
          @close="showModal = false"
      />

      <!-- Download CSV -->
      <DownloadCSV :data="tasks" />
    </main>

    <!-- Delete confirmation modal -->
    <ConfirmDeleteModal
        :show="showDeleteModal"
        message="Are you sure you want to delete this task?"
        @confirm="handleDeleteConfirm"
        @cancel="handleDeleteCancel"
    />
  </div>
</template>
