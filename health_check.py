import os
import time
import sqlite3
from datetime import datetime

def check_system_health():
    print(f"\n=== Adastra System Health Check [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ===")
    
    # Check Database module
    db_path = "database.py"
    if os.path.exists(db_path):
        print("[OK] Database module exists.")
    else:
        print("[ERROR] Database module missing!")

    # Check SQLite database file
    db_file = "adastra.db"
    if os.path.exists(db_file):
        size = os.path.getsize(db_file)
        print(f"[OK] SQLite database found. Size: {size} bytes.")
    else:
        print("[INFO] SQLite database file not created yet or using external storage.")

    print("=== Health Check Cycle Completed ===")

if __name__ == "__main__":
    print("🚀 Starting Adastra Continuous Background Health Monitor...")
    try:
        while True:
            check_system_health()
            # الانتظار لمدة 60 ثانية قبل الفحص القادم (يمكنك تعديلها حسب رغبتك)
            time.sleep(60)
    except KeyboardInterrupt:
        print("\n🛑 Health Monitor stopped gracefully by user.")


