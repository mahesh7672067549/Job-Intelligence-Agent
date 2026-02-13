import sqlite3
import time
import random
from playwright.sync_api import sync_playwright

def scrape_naukri(page, cursor):
    print("🏠 Navigating to Naukri...")
    page.goto("https://www.naukri.com/", wait_until="networkidle")
    time.sleep(2)
    page.click('input.suggestor-input')
    page.type('input.suggestor-input', "Java Python SQL Fresher", delay=100)
    page.click('div.qsbSubmit')
    time.sleep(7)
    
    # Extraction for Naukri
    elements = page.locator('a.title, a[href*="job-description"]').all()
    count = 0
    for el in elements:
        title, link = el.inner_text().strip(), el.get_attribute("href")
        if title and link:
            if not link.startswith("http"): link = "https://www.naukri.com" + link
            try:
                cursor.execute("INSERT INTO jobs (title, link) VALUES (?, ?)", (title, link))
                count += 1
            except: pass
    return count

def scrape_linkedin(page, cursor):
    # Public Job Search URL (No Login Required)
    url = "https://www.linkedin.com/jobs/search?keywords=Java%20Python%20SQL&location=India&f_TPR=r86400&position=1&pageNum=0"
    print("🔗 Navigating to LinkedIn Public Jobs...")
    page.goto(url, wait_until="load")
    time.sleep(5)
    
    # LinkedIn uses different classes (usually 'base-card__full-link')
    elements = page.locator('a.base-card__full-link').all()
    count = 0
    for el in elements:
        title, link = el.inner_text().strip(), el.get_attribute("href")
        if title and link:
            try:
                cursor.execute("INSERT INTO jobs (title, link) VALUES (?, ?)", (title, link))
                count += 1
            except: pass
    return count

def scrape_jobs():
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context("./job_profile", headless=False)
        page = browser.pages[0]
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        conn = sqlite3.connect('jobs.db')
        cursor = conn.cursor()

        n_count = scrape_naukri(page, cursor)
        print(f"✅ Naukri: Added {n_count} jobs.")
        
        time.sleep(5) # Delay between sites
        
        l_count = scrape_linkedin(page, cursor)
        print(f"✅ LinkedIn: Added {l_count} jobs.")

        conn.commit()
        conn.close()
        browser.close()

if __name__ == "__main__":
    scrape_jobs()