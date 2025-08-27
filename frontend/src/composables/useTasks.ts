import { ref } from 'vue';
import axios from 'axios';
import type { TaskItem } from "@/types/models";

export function useTasks() {
    // Список задач
    const tasks = ref<TaskItem[]>([]);
    const totalTasks = ref(0);

    // Получить список задач
    const fetchTasks = async (page = 1, pageSize = 10, status: string | null = null) => {
        try {
            const skip = (page - 1) * pageSize;
            const params: any = { skip, limit: pageSize };
            if (status) params.status = status;

            const res = await axios.get('http://localhost:8000/api/tasks', { params });

            tasks.value = res.data.tasks.map((t: TaskItem) => ({
                id: t.id,
                title: t.title,
                description: t.description,
                status: t.status,
                created_at: new Date(t.created_at),
            }));

            totalTasks.value = res.data.total;
        } catch (error) {
            console.error('Failed to fetch tasks:', error);
        }
    };

    // Удалить задачу
    const deleteTask = async (id: number) => {
        try {
            await axios.delete(`http://localhost:8000/api/tasks/${id}`);
        } catch (error) {
            console.error('Failed to delete task:', error);
        }
    };

    // Сохранить задачу (новая или редактирование)
    const saveTask = async (taskData: TaskItem, isEdit = false, taskId: number | null = null) => {
        try {
            if (isEdit && taskId) {
                await axios.put(`http://localhost:8000/api/tasks/${taskId}`, taskData);
            } else {
                await axios.post('http://localhost:8000/api/tasks', taskData);
            }
        } catch (error) {
            console.error('Failed to save task:', error);
        }
    };

    return {
        tasks,
        totalTasks,
        fetchTasks,
        deleteTask,
        saveTask,
    };
}
