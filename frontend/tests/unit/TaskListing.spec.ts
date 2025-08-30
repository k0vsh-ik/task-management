import { mount } from '@vue/test-utils'
import { ref } from 'vue'
import TaskListing from '@/components/TaskListing.vue'
import { vi } from 'vitest'

const fetchTasksMock = vi.fn()

vi.mock('@/composables/useTasks', () => ({
    useTasks: () => ({
        tasks: ref([{ id: 1, title: 'Task 1', description: 'Desc', status: 'To Do', created_at: new Date().toISOString() }]),
        totalTasks: ref(1),
        fetchTasks: fetchTasksMock,
        deleteTask: vi.fn(),
        saveTask: vi.fn()
    })
}))

vi.mock('@/composables/useTaskWS', () => ({
    useTaskWS: vi.fn()
}))

describe('TaskListing.vue', () => {
    beforeEach(() => {
        fetchTasksMock.mockClear() // сбрасываем вызовы перед каждым тестом
    })

    it('calls fetchTasks on mount', () => {
        mount(TaskListing)
        expect(fetchTasksMock).toHaveBeenCalled()
    })

    it('opens modal when "+ Add Task" button is clicked', async () => {
        const wrapper = mount(TaskListing)
        const button = wrapper.find('button')
        await button.trigger('click')
        expect(wrapper.html()).toContain('Add New Task')
    })

    it('calls fetchTasks when status filter changes', async () => {
        const wrapper = mount(TaskListing)
        const select = wrapper.find('select')
        await select.setValue('Done')
        expect(fetchTasksMock).toHaveBeenCalledTimes(2) // 1 раз на mount, 1 раз при фильтре
    })
})
