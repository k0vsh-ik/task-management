import { mount } from '@vue/test-utils'
import Task from '@/components/Task.vue'

describe('Task.vue', () => {
    const mockTask = {
        id: 1,
        title: 'Test Task',
        description: 'Test Description',
        status: 'In Progress',
        created_at: '2025-08-29T10:00:00Z'
    }

    it('renders task data correctly', () => {
        const wrapper = mount(Task, {
            props: { task: mockTask }
        })

        expect(wrapper.text()).toContain('Test Task')
        expect(wrapper.text()).toContain('Test Description')
        expect(wrapper.text()).toContain('In Progress')
    })

    it('applies correct class for status', () => {
        const wrapper = mount(Task, {
            props: { task: mockTask }
        })
        const span = wrapper.find('span')
        expect(span.classes()).toContain('bg-yellow-100') // for In Progress
    })

    it('emits "edit" event when edit button is clicked', async () => {
        const wrapper = mount(Task, { props: { task: mockTask } })
        await wrapper.find('button.text-blue-600').trigger('click')
        expect(wrapper.emitted('edit')).toBeTruthy()
        expect(wrapper.emitted('edit')![0]).toEqual([mockTask])
    })

    it('emits "delete" event when delete button is clicked', async () => {
        const wrapper = mount(Task, { props: { task: mockTask } })
        await wrapper.find('button.text-red-600').trigger('click')
        expect(wrapper.emitted('delete')).toBeTruthy()
        expect(wrapper.emitted('delete')![0]).toEqual([mockTask.id])
    })
})
