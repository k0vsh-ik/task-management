import { ref } from 'vue';
import axios from 'axios';
import type { TaskItem } from "@/types/models";

const API_URL = import.meta.env.VITE_API_URL;

export function useTasks() {
    const tasks = ref<TaskItem[]>([]);
    const totalTasks = ref(0);

    const fetchTasks = async (page = 1, pageSize = 10, status: string | null = null) => {
        const skip = (page - 1) * pageSize;
        const params: any = { skip, limit: pageSize };
        if (status) params.status = status;
        const res = await axios.get(`${API_URL}/api/tasks`, { params });
        tasks.value = res.data.tasks.map((t: TaskItem) => ({
            ...t,
            created_at: new Date(t.created_at),
        }));
        totalTasks.value = res.data.total;
    };

    const deleteTask = async (id: number) => {
        await axios.delete(`${API_URL}/api/tasks/${id}`);
    };

    const saveTask = async (taskData: TaskItem, isEdit = false, taskId: number | null = null) => {
        if (isEdit && taskId) {
            await axios.put(`${API_URL}/api/tasks/${taskId}`, taskData);
        } else {
            await axios.post(`${API_URL}/api/tasks`, taskData);
        }
    };

    return { tasks, totalTasks, fetchTasks, deleteTask, saveTask };
}
