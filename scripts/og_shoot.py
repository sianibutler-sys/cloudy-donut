# Renders og-mockups.html cards to 1200x630 JPEGs in og/. Run by the og-images GitHub workflow.
import asyncio, sys
from playwright.async_api import async_playwright
CARDS = ["pop-ups", "locations", "flavors", "home-corner"]
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1200, "height": 630})
        for c in CARDS:
            await pg.goto(f"file://{sys.argv[1]}/og-mockups.html?card={c}")
            await pg.wait_for_load_state("networkidle")
            await pg.evaluate("document.fonts.ready")
            await pg.wait_for_timeout(800)
            out = "index" if c == "home-corner" else c
            await pg.locator(f'.cell.on .og').screenshot(path=f"og/{out}.jpg", type="jpeg", quality=86)
        await b.close()
asyncio.run(main())
