import { ref } from 'vue';
import axios from 'axios';

export function useTasks() {
    // Reactive state
    const tasks = ref([]);
    const totalTasks = ref(0);

    // Fetch tasks with pagination and optional status filter
    const fetchTasks = async (page = 1, pageSize = 10, status: string | null = null) => {
        try {
            const skip = (page - 1) * pageSize;
            const params: any = { skip, limit: pageSize };
            if (status) params.status = status; // Add status filter if provided

            const res = await axios.get('http://localhost:8000/api/tasks', { params });

            tasks.value = res.data.tasks.map(t => ({
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

    // Delete a task by ID
    const deleteTask = async (id) => {
        try {
            await axios.delete(`http://localhost:8000/api/tasks/${id}`);
        } catch (error) {
            console.error('Failed to delete task:', error);
        }
    };

    // Save a task (add or edit)
    const saveTask = async (taskData, isEdit = false, taskId = null) => {
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
