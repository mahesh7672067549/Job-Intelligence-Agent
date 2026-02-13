import requests

def send_telegram_notification(job_summary):
    # REPLACE with your real data
    BOT_TOKEN = "8498941302:AAHWz7eb3Ik_A5cbx1SHgHseyS9HtUR1OTM"
    CHAT_ID = "5212208140"
    
    # Format the message for better reading
    header = "🚀 *mahesh's Daily Job Scout* 🚀\n\n"
    message = header + job_summary
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown" # Makes the text bold/pretty
    }
    
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("✅ Notification sent to your phone!")
        else:
            print(f"❌ Failed to send: {response.text}")
    except Exception as e:
        print(f"❌ Connection error: {e}")

# --- Quick Test ---
if __name__ == "__main__":
    # Test with the output your brain just gave you
    test_data = "1. Junior Java Developer (Fresher)\n2. Software Engineering Intern - Python"
    send_telegram_notification(test_data)