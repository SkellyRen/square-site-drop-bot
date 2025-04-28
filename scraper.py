import os
import time
import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Load environment variables ---
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
SQUARE_SUBDOMAIN = os.getenv("SQUARE_SUBDOMAIN")
STORE_NAME = os.getenv("STORE_NAME", SQUARE_SUBDOMAIN)  # fallback to subdomain if not set

# --- Build URLs ---
URL = f"https://{SQUARE_SUBDOMAIN}.square.site/s/shop?page=1&limit=200&sort_by=created_date&sort_order=desc"
SHOP_LINK = f"https://{SQUARE_SUBDOMAIN}.square.site/s/shop"

SEEN_ITEMS_FILE = "seen_items.txt"

# --- Setup headless Chrome ---
CHROME_BINARY = os.getenv("CHROME_BINARY", "/usr/bin/google-chrome")
CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH", "/usr/local/bin/chromedriver")

options = Options()
options.binary_location = CHROME_BINARY
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service(executable_path=CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

# --- Load previously seen items ---
if os.path.exists(SEEN_ITEMS_FILE):
    with open(SEEN_ITEMS_FILE, "r") as f:
        seen_items = set(f.read().splitlines())
else:
    seen_items = set()

# --- Visit the page and scrape products ---
driver.get(URL)
try:
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/product/']"))
    )
except Exception as e:
    print("❌ Timeout waiting for product elements to load:", e)

soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

product_links = soup.select("a[href*='/product/']")
print(f"Found {len(product_links)} product links")

new_items = []

for link in product_links:
    name = link.get_text(strip=True)
    href = f"https://{SQUARE_SUBDOMAIN}.square.site{link['href']}"

    if href not in seen_items and name:
        new_items.append((name, href))
        seen_items.add(href)

# --- Prepare and send Discord messages ---
if new_items:
    MAX_LENGTH = 1900
    description = f"📦 {len(new_items)} new items added to {STORE_NAME}:\n\n"
    batches = []

    for name, url in new_items:
        price = None
        if "$" in name:
            parts = name.rsplit("$", 1)
            if len(parts) == 2:
                name, price = parts
                price = f"${price.strip()}"

        line = f"• [{name.strip()}]({url})"
        if price:
            line += f" — {price}"
        line += "\n"

        if len(description) + len(line) + 60 > MAX_LENGTH:
            description += f"\n_And more! [View all →]({SHOP_LINK})_"
            batches.append(description.strip())
            description = ""

        if not description:
            description = ""

        description += line

    if description:
        batches.append(description.strip())

    # Send each batch
    for idx, batch in enumerate(batches):
        title = f"🆕 New Drop from {STORE_NAME}!"
        if len(batches) > 1:
            title += f" (Part {idx + 1}/{len(batches)})"

        payload = {
            "embeds": [
                {
                    "title": title,
                    "description": batch,
                    "color": 0x00ffcc
                }
            ]
        }

        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        if response.status_code == 204:
            print(f"✅ Posted batch {idx + 1}/{len(batches)} to Discord")
        else:
            print(f"❌ Failed posting batch {idx + 1}: {response.status_code} - {response.text}")

        time.sleep(1)

else:
    # No new items
    payload = {
        "content": "📭 No new items found in this drop cycle."
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    if response.status_code == 204:
        print("✅ Posted 'no new items' message to Discord")
    else:
        print(f"❌ Failed to post: {response.status_code} - {response.text}")

# --- Save updated seen items ---
with open(SEEN_ITEMS_FILE, "w") as f:
    for item in seen_items:
        f.write(f"{item}\n")
