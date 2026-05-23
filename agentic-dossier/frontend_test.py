from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch()
    page = browser.new_page()
    page.goto("http://localhost:3000")

    # Upload dummy file
    page.locator("#pdf-upload").set_input_files("dummy.txt")

    # Click submit
    page.locator("#submit-btn").click()

    # Wait for the status message to update to "All selected files processed."
    page.locator("#status-message").wait_for(state="visible", timeout=5000)
    page.wait_for_selector('text="All selected files processed."')

    # Wait a bit more to ensure console output is rendered
    page.wait_for_timeout(1000)

    # Take screenshot
    page.screenshot(path="screenshot.png")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
