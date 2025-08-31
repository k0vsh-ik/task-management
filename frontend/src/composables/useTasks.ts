import { ref } from 'vue';
import axios from 'axios';
import type { TaskItem } from "@/types/models";

const API_URL = import.meta.env.VITE_API_URL;

export function useTasks() {
    const tasks = ref<TaskItem[]>([]);
    const totalTasks = ref(0);
    const message = ref<string | null>(null);
    const isError = ref(false);

    const showMessage = (text: string, error = false) => {
        message.value = text;
        isError.value = error;
        setTimeout(() => {
            message.value = null;
        }, 3000);
    };

    const fetchTasks = async (page = 1, pageSize = 10, status: string | null = null) => {
        try {
            const skip = (page - 1) * pageSize;
            const params: any = { skip, limit: pageSize };
            if (status) params.status = status;
            const res = await axios.get(`${API_URL}/api/tasks`, { params });
            tasks.value = res.data.tasks.map((t: TaskItem) => ({
                ...t,
                created_at: new Date(t.created_at),
            }));
            totalTasks.value = res.data.total;
        } catch (err) {
            showMessage('Loading Task Error', true);
        }
    };

    const deleteTask = async (id: number) => {
        try {
            await axios.delete(`${API_URL}/api/tasks/${id}`);
            showMessage('Task is deleted successfully');
            await fetchTasks();
        } catch (err) {
            showMessage('Deleting Task Error', true);
        }
    };

    const saveTask = async (taskData: TaskItem, isEdit = false, taskId: number | null = null) => {
        try {
            if (isEdit && taskId) {
                await axios.put(`${API_URL}/api/tasks/${taskId}`, taskData);
                showMessage('Task is edited successfully');
            } else {
                await axios.post(`${API_URL}/api/tasks`, taskData);
                showMessage('Task is created successfully');
            }
            await fetchTasks();
        } catch (err) {
            showMessage('Saving Task Error', true);
        }
    };

    return {
        tasks,
        totalTasks,
        message,
        isError,
        fetchTasks,
        deleteTask,
        saveTask
    };
}
