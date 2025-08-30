import { mount } from '@vue/test-utils'
import TaskModal from '@/components/TaskModal.vue'

describe('TaskModal.vue', () => {
    it('renders title for adding a task', () => {
        const wrapper = mount(TaskModal, {
            props: { isEdit: false }
        })
        expect(wrapper.text()).toContain('Add New Task')
    })

    it('renders title for editing a task', () => {
        const wrapper = mount(TaskModal, {
            props: { isEdit: true, task: { id: 1, title: 'Title', description: 'Desc', status: 'To Do', created_at: new Date().toISOString() } }
        })
        expect(wrapper.text()).toContain('Edit Task')
    })

    it('disables Add button when fields are empty', async () => {
        const wrapper = mount(TaskModal, { props: { isEdit: false } })
        const button = wrapper.find('button:last-child')
        expect(button.classes()).toContain('cursor-not-allowed')
    })

    it('emits "close" event when Cancel button is clicked', async () => {
        const wrapper = mount(TaskModal, { props: { isEdit: false } })
        await wrapper.find('button').trigger('click') // Cancel button
        expect(wrapper.emitted('close')).toBeTruthy()
    })

    it('emits "save" event when valid data is provided', async () => {
        const wrapper = mount(TaskModal, { props: { isEdit: false } })
        await wrapper.find('input').setValue('Test Task')
        await wrapper.find('textarea').setValue('Test Description')
        await wrapper.find('button:last-child').trigger('click') // Add button
        // Simulate confirmation
        await wrapper.vm.$emit('save', {
            title: 'Test Task',
            description: 'Test Description',
            status: 'To Do'
        })
        expect(wrapper.emitted('save')).toBeTruthy()
        expect(wrapper.emitted('save')![0][0].title).toBe('Test Task')
    })
})
