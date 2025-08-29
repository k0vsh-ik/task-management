import { onMounted, onUnmounted } from "vue";
import type { Ref } from "vue";
import type { TaskItem } from "@/types/models";

export function useTaskWS(
    taskList: Ref<TaskItem[]>,
    totalTasks: Ref<number>,
    currentPage: Ref<number>,
    pageSize: Ref<number>,
    statusFilter: Ref<string | null>,
    fetchTasks: (page: number, pageSize: number, status: string | null) => Promise<void>
) {
    let socket: WebSocket | null = null;

    onMounted(() => {
        const wsUrl = import.meta.env.VITE_API_URL.replace(/^http/, "ws") + "/ws/tasks";
        socket = new WebSocket(wsUrl);

        socket.onmessage = async (event) => {
            const data = JSON.parse(event.data);
            console.log("Received data", data);
            const { event: evt, task, task_id } = data;

            const passesFilter = !statusFilter.value || (task?.status === statusFilter.value);

            switch (evt) {
                case "created":
                case "updated":
                case "deleted":
                    // Перезагружаем текущую страницу после любого события
                    await fetchTasks(currentPage.value, pageSize.value, statusFilter.value);
                    break;
            }
        };
    });

    onUnmounted(() => {
        socket?.close();
    });
}
