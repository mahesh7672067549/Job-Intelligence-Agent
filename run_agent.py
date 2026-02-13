import sqlite3
import time
# Importing the functions you built in previous steps
from scout import scrape_jobs 
from brain import filter_jobs
from notifier import send_telegram_notification

def main():
    print("🚀 JOB AGENT: Starting daily routine...")

    # 1. THE SCOUT: Go to the web and find raw links
    print("🔍 Step 1: Scouting job boards...")
    scrape_jobs() 

    # 2. THE MEMORY: Pull the new jobs from your SQL database
    conn = sqlite3.connect('jobs.db')
    cursor = conn.cursor()
    # We only want jobs that haven't been sent to your phone yet (notified = 0)
    cursor.execute("SELECT title, link FROM jobs WHERE notified = 0")
    new_rows = cursor.fetchall()
    
    if not new_rows:
        print("😴 No new jobs found since the last run. Closing agent.")
        conn.close()
        return

    print(f"📈 Found {len(new_rows)} new listings. Consulting the Brain...")

    # 3. THE BRAIN: Send the titles to Gemini for filtering
    job_list_for_ai = [f"Title: {row[0]} | Link: {row[1]}" for row in new_rows]
    ai_recommendations = filter_jobs(job_list_for_ai)

    # 4. THE VOICE: Send the final 'Top Picks' to your Telegram
    print("📱 Sending recommendations to Telegram...")
    send_telegram_notification(ai_recommendations)

    # 5. UPDATE: Mark these jobs as 'notified' so you don't see them again tomorrow
    cursor.execute("UPDATE jobs SET notified = 1 WHERE notified = 0")
    conn.commit()
    conn.close()
    
    print("🎯 Task Complete. Check your phone!")

if __name__ == "__main__":
    main()