<script setup lang="ts">
import type { TaskItem } from "@/types/models";

const API_URL = import.meta.env.VITE_MICROSERVICE_URL || "http://localhost:8080";

defineProps<{ data: TaskItem[] }>();

async function downloadCSV(data: TaskItem[]) {
  try {
    const response = await fetch(`${API_URL}/convert`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    if (!response.ok) throw new Error("Failed to download CSV");

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "data.csv";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  } catch (err) {
    alert(err instanceof Error ? err.message : "Unknown error");
  }
}
</script>

<template>
  <div>
    <button @click="downloadCSV($props.data)" class="pi pi-download">
      Download CSV
    </button>
  </div>
</template>
