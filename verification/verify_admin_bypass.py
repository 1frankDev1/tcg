import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Access admin.html
        # Since I'm in a sandbox, I'll use a file path if possible or start a server.
        # Given previous steps, I can assume the server might be running or I can just open the file.
        # But wait, JS modules and fetch might need a server.

        # Start a simple web server
        process = await asyncio.create_subprocess_exec(
            'python3', '-m', 'http.server', '8081', '--directory', 'docs'
        )
        await asyncio.sleep(2)

        try:
            await page.goto('http://localhost:8081/admin.html')
            await page.wait_for_timeout(3000) # Wait for JS to run and bypass login

            await page.screenshot(path='verification/screenshots/admin_dashboard_bypassed.png', full_page=True)
            print("Admin dashboard (bypassed) screenshot saved.")

        finally:
            process.terminate()
            await process.wait()

        await browser.close()

if __name__ == "__main__":
    os.makedirs('verification/screenshots', exist_ok=True)
    asyncio.run(main())
