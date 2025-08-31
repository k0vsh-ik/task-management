<script setup lang="ts">
import { ref, computed, onMounted, watch } from "vue";
import type { TaskItem } from "@/types/models";
import { useTasks } from "@/composables/useTasks";
import { useTaskWS } from "@/composables/useTaskWS";

import Pagination from "@/components/Pagination.vue";
import Task from "@/components/Task.vue";
import TaskModal from "@/components/TaskModal.vue";
import ConfirmDeleteModal from "@/components/ConfirmDeleteModal.vue";
import DownloadCSV from "@/components/DownloadCSV.vue";
import Notification from "@/components/Notification.vue";

// ---------------------------------
// Tasks composable
// ---------------------------------
const { tasks, totalTasks, fetchTasks, deleteTask, saveTask, message, isError } = useTasks();

// ---------------------------------
// Pagination & Filter
// ---------------------------------
const currentPage = ref(1);
const pageSize = ref(10);
const totalPages = computed(() => Math.ceil(totalTasks.value / pageSize.value));

const statusFilter = ref<string | null>(null);
const statusOptions = ["To Do", "In Progress", "Done"];

// ---------------------------------
// Modal & Editing
// ---------------------------------
const showModal = ref(false);
const isEditing = ref(false);
const editingTask = ref<TaskItem | null>(null);

const showDeleteModal = ref(false);
const taskToDelete = ref<number | null>(null);

// ---------------------------------
// WebSocket
// ---------------------------------
useTaskWS(tasks, totalTasks, currentPage, pageSize, statusFilter, fetchTasks);

// ---------------------------------
// Initial fetch
// ---------------------------------
onMounted(() => fetchTasks(currentPage.value, pageSize.value, statusFilter.value));

// ---------------------------------
// Watch status filter
// ---------------------------------
watch(statusFilter, async () => {
  currentPage.value = 1;
  await fetchTasks(currentPage.value, pageSize.value, statusFilter.value);
});

// ---------------------------------
// Pagination handler
// ---------------------------------
async function onPageChange(page: number) {
  currentPage.value = page;
  await fetchTasks(page, pageSize.value, statusFilter.value);
}

// ---------------------------------
// CRUD handlers
// ---------------------------------
function openAddModal() {
  isEditing.value = false;
  editingTask.value = null;
  showModal.value = true;
}

function openEditModal(task: TaskItem) {
  isEditing.value = true;
  editingTask.value = task;
  showModal.value = true;
}

async function handleSave(taskData: TaskItem) {
  await saveTask(taskData, isEditing.value, editingTask.value?.id ?? null);
  showModal.value = false;
  editingTask.value = null;

  await fetchTasks(currentPage.value, pageSize.value, statusFilter.value);
}

function confirmDelete(taskId: number) {
  taskToDelete.value = taskId;
  showDeleteModal.value = true;
}

async function handleDeleteConfirm() {
  if (taskToDelete.value !== null) {
    await deleteTask(taskToDelete.value);
    showDeleteModal.value = false;
    taskToDelete.value = null;

    await fetchTasks(currentPage.value, pageSize.value, statusFilter.value);
  }
}

function handleDeleteCancel() {
  taskToDelete.value = null;
  showDeleteModal.value = false;
}
</script>

<template>
  <div class="min-h-screen flex flex-col items-center">
    <Notification :message="message" :isError="isError" />

    <div class="flex flex-col justify-center h-1/2 w-full max-w-5xl p-6">
      <div class="flex justify-between items-center">
        <h2 class="text-2xl font-bold text-gray-700">Your Tasks</h2>
        <button
            @click="openAddModal"
            class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
        >
          + Add Task
        </button>
      </div>
    </div>

    <main class="w-full max-w-5xl pl-6 pr-6 pb-6 bg-white rounded-lg shadow-lg">
      <!-- Tasks table -->
      <div class="overflow-x-auto">
        <table class="min-w-full border border-gray-200 rounded-lg overflow-hidden">
          <thead class="bg-gray-100">
          <tr>
            <th class="px-4 py-2 text-left text-gray-700 font-semibold">ID</th>
            <th class="px-4 py-2 text-left text-gray-700 font-semibold">Title</th>
            <th class="px-4 py-2 text-left text-gray-700 font-semibold">Description</th>
            <th class="px-4 py-2 text-left text-gray-700 font-semibold">
              <select v-model="statusFilter" class="border rounded px-2 py-1">
                <option :value="null">Status</option>
                <option v-for="status in statusOptions" :key="status" :value="status">
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
      <Pagination class="pt-6"
          :currentPage="currentPage"
          :totalPages="totalPages"
          @changePage="onPageChange"
      />

      <div class="text-center mt-2 text-gray-600">
        Total Tasks: {{ totalTasks }}
      </div>

      <!-- Task Modal -->
      <TaskModal
          v-if="showModal"
          :task="editingTask"
          :isEdit="isEditing"
          @save="handleSave"
          @close="showModal = false"
      />

      <!-- Delete Confirmation Modal -->
      <ConfirmDeleteModal
          v-if="showDeleteModal"
          :show="showDeleteModal"
          message="Are you sure you want to delete this task?"
          @confirm="handleDeleteConfirm"
          @cancel="handleDeleteCancel"
      />

      <DownloadCSV :data="tasks" />
    </main>
  </div>
</template>
