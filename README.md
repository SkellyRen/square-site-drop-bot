# 📢 Square.site Item Checker Bot

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Discord](https://img.shields.io/badge/Discord-Bot-blueviolet)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

A GitHub Actions bot that monitors a Square.site store for **new product drops** and posts a **summary** to a Discord channel twice daily.

---

## 🛠️ How It Works
- Scrapes the Square Online shop page using **Selenium** and **BeautifulSoup**
- Tracks previously seen items (`seen_items.txt`)
- If new items are found:
  - Posts an embed to Discord with item names, prices, and clickable links
  - Auto-splits into multiple posts if needed to stay within Discord limits
- If no new items are found:
  - Posts a clean "No new items found" message

---

## 💡 Features
- Clean Discord embeds with clickable product links
- 1-second delay between posts to avoid Discord rate limits
- Auto-batching if a large number of new items are found
- Supports **any** Square Online store via subdomain
- Light, fast, reliable

---

## 🌐 Live Schedule (UTC)
| Local Time (Central) | UTC Time (for GitHub Actions cron) |
|:---------------------|:----------------------------------|
| 12:00 PM             | 5:00 PM UTC                      |
| 6:00 PM              | 11:00 PM UTC                     |

> **GitHub Actions schedules are always in UTC.**

---

## 🛠 Setup Instructions

1. **Clone the repository**
2. **Set up GitHub Actions Secret**:
   - `DISCORD_WEBHOOK_URL` → Your Discord webhook URL
3. **Set up GitHub Actions Variables**:
   - `SQUARE_SUBDOMAIN` → Your store's subdomain (example: `examplestore` for `examplestore.square.site`)
   - `STORE_NAME` → (Optional) Friendly name for your store in Discord posts
4. **Workflow** already provided (`.github/workflows/new-item-check.yml`)
5. **No need for `requirements.txt`** — dependencies are installed directly inside the GitHub Actions job.
6. Done! The bot will scrape & post automatically twice daily.

⚙️ GitHub Actions Settings: Ensure “Read and Write” permissions are enabled for GitHub Actions in your repository settings.

---

## 🔍 Tech Stack
- Python 3.10+
- Selenium (headless Chrome)
- BeautifulSoup (HTML parsing)
- Discord Webhook API
- GitHub Actions (scheduling & automation)

---

## 📅 Future Ideas
- Add product **images** to embeds
- Smarter detection if the store is closed or empty
- Enhanced timezone handling
- Optional summary post of all drops at the end of the day

---

## 🚀 Author
Built by [@SkellyRen](https://github.com/SkellyRen) to make item drops easier to track 🎶

---

## ⚡ License
This project is licensed under the **MIT License**.  
See [LICENSE](LICENSE) for full details.  
Please scrape respectfully — check stores gently and avoid aggressive scraping behaviors.
