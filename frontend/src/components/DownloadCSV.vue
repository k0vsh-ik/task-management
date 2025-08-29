<script setup lang="ts">
import type { TaskItem } from "@/types/models";

const API_URL = import.meta.env.VITE_MICROSERVICE_URL;

interface Record {
  name: string;
  age: number;
  city: string;
}

// Define component props
const props = defineProps<{
  data: TaskItem[];
}>();

// Download data as CSV
async function downloadCSV() {
  console.log(props.data);

  const response = await fetch(`${API_URL}/convert`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(props.data)
  });

  if (!response.ok) {
    alert("Failed to download CSV");
    return;
  }

  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "data.csv";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  window.URL.revokeObjectURL(url);
}
</script>

<template>
  <div>
    <button @click="downloadCSV" class="pi pi-download">
      Download CSV
    </button>
  </div>
</template>
