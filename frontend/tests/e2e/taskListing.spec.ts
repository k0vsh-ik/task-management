import { test, expect } from '@playwright/test'

test.describe('TaskListing', () => {
    test.beforeEach(async ({ page }) => {
        await page.goto('http://localhost:5173')
    })

    test('opens modal when "+ Add Task" is clicked', async ({ page }) => {
        await page.click('text="+ Add Task"')
        await expect(page.locator('text=Add New Task')).toBeVisible()
    })

    test('creates a new task', async ({ page }) => {
        await page.click('text="+ Add Task"')
        await page.fill('input[placeholder="Title"]', 'New Test Task')
        await page.fill('textarea[placeholder="Description"]', 'Task description')
        await page.click('button[name="submit"]')
        await page.click('button[name="confirmSaveButton"]')
        await expect(page.locator('text=New Test Task').first()).toBeVisible()
    })
})
