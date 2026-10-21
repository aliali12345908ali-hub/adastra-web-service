import csv
import os

LEADS_FILE = "enterprise_leads.csv"

def process_outreach():
    if not os.path.exists(LEADS_FILE):
        print("❌ لم يتم العثور على ملف العملاء enterprise_leads.csv")
        return

    print("🚀 بدء تجهيز رسائل العروض للعملاء الكبار B2B...\n")
    with open(LEADS_FILE, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            company = row.get("Company Name")
            email = row.get("Email")
            status = row.get("Status")
            
            print(f"📧 جاهز للإرسال إلى: {company} | الإيميل: {email} | الحالة: {status}")

if __name__ == "__main__":
    process_outreach()
