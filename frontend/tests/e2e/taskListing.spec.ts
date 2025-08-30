import { test, expect } from '@playwright/test'

test.describe('TaskListing', () => {
    test.beforeEach(async ({ page }) => {
        await page.goto('http://localhost:5173') // адрес dev-сервера
    })

    test('opens modal when "+ Add Task" is clicked', async ({ page }) => {
        await page.click('text="+ Add Task"')
        await expect(page.locator('text=Add New Task')).toBeVisible()
    })

    test('creates a new task', async ({ page }) => {
        await page.click('text="+ Add Task"')
        await page.fill('input[name="title"]', 'New Test Task')
        await page.fill('textarea[name="description"]', 'Task description')
        await page.click('button[name="savebtn"]')
        await page.click('button[name="confirmbtn"]')
        await expect(page.locator('text=New Test Task').first()).toBeVisible()
    })
})
