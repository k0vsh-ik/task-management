import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
    testDir: './tests/e2e',   // folder with your e2e tests
    timeout: 30 * 1000,        // maximum time per test
    retries: 1,                // retry once if test fails
    use: {
        browserName: 'chromium', // you can use 'firefox' or 'webkit'
        headless: true,           // false if you want to see the browser
        screenshot: 'only-on-failure',
        trace: 'on-first-retry',
    },
    projects: [
        {
            name: 'safari',
            use: { ...devices['Desktop Safari'] },
        },
    ],
})
