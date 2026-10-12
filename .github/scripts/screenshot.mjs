// Captures the above-the-fold view of a site for the README.
// Usage: node screenshot.mjs <url> <output.jpg>
import { chromium } from "playwright";

const [url, out] = process.argv.slice(2);
if (!url || !out) {
  console.error("usage: node screenshot.mjs <url> <output.jpg>");
  process.exit(1);
}

const browser = await chromium.launch();
const page = await browser.newPage({
  viewport: { width: 1280, height: 651 },
  colorScheme: "dark",
});
await page.goto(url, { waitUntil: "networkidle", timeout: 60_000 });
// Let entrance animations and lazy-loaded hero images settle.
await page.waitForTimeout(3000);
await page.screenshot({ path: out, type: "jpeg", quality: 85 });
await browser.close();
console.log(`saved ${url} -> ${out}`);
