<script setup lang="ts">
import type { TaskItem } from "@/types/models";
import { ref } from "vue";
import Notification from "@/components/Notification.vue";

const API_URL = import.meta.env.VITE_MICROSERVICE_URL || "http://localhost:8080";

defineProps<{ data: TaskItem[] }>();

const message = ref<string | null>(null);
const isError = ref(false);

async function downloadCSV(data: TaskItem[]) {
  try {
    const response = await fetch(`${API_URL}/convert`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "data.csv";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);

    message.value = "CSV downloaded successfully!";
    isError.value = false;

  } catch (err) {
    message.value = err instanceof Error ? err.message : "Unknown error";
    isError.value = true;

  } finally {
    setTimeout(() => (message.value = null), 3000);
  }
}
</script>

<template>
  <div>
    <button @click="downloadCSV($props.data)" class="pi pi-download">
      Download CSV
    </button>

    <Notification :message="message" :isError="isError" />
  </div>
</template>
