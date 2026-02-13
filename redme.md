import sqlite3
import time
from playwright.sync_api import sync_playwright

def scrape_jobs():
    url = "https://www.naukri.com/java-python-sql-fresher-jobs"
    
    with sync_playwright() as p:
        # headless=False lets you watch it find the jobs
        browser = p.chromium.launch(headless=False) 
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        print(f"🌐 Navigating to: {url}")
        
        try:
            page.goto(url, wait_until="load", timeout=60000)
            print("⏳ Waiting for content...")
            time.sleep(7)
            
            # SCROLL DOWN: Naukri only loads jobs when you scroll
            print("📜 Scrolling to load more jobs...")
            for _ in range(3):
                page.mouse.wheel(0, 800)
                time.sleep(2)

            # --- DYNAMIC SELECTOR LIST ---
            # This looks for Naukri's current CSS classes for job titles
            selectors = [
                'a.title', 
                'a[href*="job-description"]', 
                '.jobTuple.bgWhite a.title',
                'div.cust-job-tuple a'
            ]
            
            job_elements = []
            for selector in selectors:
                found = page.locator(selector).all()
                job_elements.extend(found)
                if found:
                    print(f"🎯 Found matches using selector: {selector}")

            conn = sqlite3.connect('jobs.db')
            cursor = conn.cursor()
            
            added_count = 0
            # Use a set to avoid processing the same element twice in one run
            seen_in_this_run = set()

            for el in job_elements:
                try:
                    title = el.inner_text().strip()
                    link = el.get_attribute("href")
                    
                    if title and link and link not in seen_in_this_run:
                        seen_in_this_run.add(link)
                        
                        # Ensure link is absolute
                        if not link.startswith("http"):
                            link = "https://www.naukri.com" + link
                        
                        # Only add tech-looking titles
                        if len(title) > 5:
                            cursor.execute("INSERT INTO jobs (title, link) VALUES (?, ?)", (title, link))
                            added_count += 1
                except:
                    continue
            
            conn.commit()
            conn.close()
            print(f"✅ Successfully extracted and saved {added_count} new jobs.")
            
        except Exception as e:
            print(f"❌ Error during scouting: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    scrape_jobs()