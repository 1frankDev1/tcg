import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        process = await asyncio.create_subprocess_exec(
            'python3', '-m', 'http.server', '8082', '--directory', 'docs'
        )
        await asyncio.sleep(2)
        try:
            # Using a real identifier from the code or just bypass
            await page.goto('http://localhost:8082/public.html?id=Diseñador&view=albums')
            await page.wait_for_timeout(3000)
            await page.screenshot(path='verification/screenshots/public_albums_redesign.png', full_page=True)

            # Hover over the menu
            await page.hover('.public-nav')
            await page.wait_for_timeout(1000)
            await page.screenshot(path='verification/screenshots/public_menu_hover.png')

            print("Public screenshots saved.")
        finally:
            process.terminate()
            await process.wait()
        await browser.close()

if __name__ == "__main__":
    os.makedirs('verification/screenshots', exist_ok=True)
    asyncio.run(main())
