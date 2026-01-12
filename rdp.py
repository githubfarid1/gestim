from playwright.sync_api import sync_playwright, Playwright

def run(playwright: Playwright):
    # Connect to the existing browser instance via CDP
    browser = playwright.chromium.connect_over_cdp("http://localhost:9222")
    
    # Access the default context and existing pages, or create a new page
    default_context = browser.contexts[0]
    # If a page already exists in the context, you can access it like below
    # page = default_context.pages[0] 
    
    # Alternatively, create a new page in the default context
    page = default_context.new_page()

    # Perform automation actions
    page.goto("https://www.google.com/")
    print(f"Page title: {page.title()}")
    
    # Note: Playwright connects to the existing session, the browser process itself 
    # must be closed manually or through an external process management in this scenario.

with sync_playwright() as playwright:
    run(playwright)
