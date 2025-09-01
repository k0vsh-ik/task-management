import { onMounted, onUnmounted } from "vue";
import type { Ref } from "vue";
import type { TaskItem } from "@/types/models";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export function useTaskWS(
    taskList: Ref<TaskItem[]>,
    totalTasks: Ref<number>,
    currentPage: Ref<number>,
    pageSize: Ref<number>,
    statusFilter: Ref<string | null>,
    fetchTasks: (page: number, pageSize: number, status: string | null) => Promise<void>
) {
    let socket: WebSocket | null = null;

    const handleMessage = async (event: MessageEvent) => {
        try {
            const data = JSON.parse(event.data);
            const { event: evt, task} = data;
            console.log("Received data:", data);

            const passesFilter = !statusFilter.value || task?.status === statusFilter.value;

            if (!passesFilter) return;

            if (["created", "updated", "deleted"].includes(evt)) {
                await fetchTasks(currentPage.value, pageSize.value, statusFilter.value);
            }
        } catch (err) {
            console.error("Error handling WS message:", err);
        }
    };

    onMounted(() => {
        const wsUrl = API_URL.replace(/^http/, "ws") + "/ws/tasks";
        socket = new WebSocket(wsUrl);
        socket.onmessage = handleMessage;
    });

    onUnmounted(() => {
        socket?.close();
    });
}
