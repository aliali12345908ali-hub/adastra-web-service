import os
import sqlite3
from datetime import datetime

def check_system_health():
    print("=== Adastra System Health Check ===")
    print(f"Time: {datetime.now()}")
    
    # Check Database file
    db_path = "database.py"
    if os.path.exists(db_path):
        print("[OK] Database module exists.")
    else:
        print("[ERROR] Database module missing!")

    # Check SQLite connection / file if exists
    db_file = "adastra.db"
    if os.path.exists(db_file):
        size = os.path.getsize(db_file)
        print(f"[OK] SQLite database found. Size: {size} bytes.")
    else:
        print("[INFO] SQLite database file not created yet or using external storage.")

    print("=== Health Check Completed Successfully ===")

if __name__ == "__main__":
    check_system_health()

