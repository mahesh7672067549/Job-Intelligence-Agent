import sqlite3

def clear_database():
    try:
        # Connect to your specific database
        conn = sqlite3.connect('jobs.db')
        cursor = conn.cursor()

        # This wipes the data but keeps the 'jobs' table ready
        cursor.execute("DELETE FROM jobs")

        conn.commit()
        conn.close()
        print("🧹 Success: Database cleared! Ready for fresh links.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    clear_database()