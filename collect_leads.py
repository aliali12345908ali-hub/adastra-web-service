import csv
import os

LEADS_FILE = "enterprise_leads.csv"

def init_db():
    if not os.path.exists(LEADS_FILE):
        with open(LEADS_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Company Name", "Email", "Status"])
        print("✅ تم إنشاء ملف قاعدة البيانات: enterprise_leads.csv")

def add_lead(company_name, email):
    with open(LEADS_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([company_name, email, "Pending"])
    print(f"🎯 تم إضافة العميل بنجاح: {company_name} ({email})")

def show_leads():
    print("\n📊 قائمة العملاء المستهدفين:")
    if os.path.exists(LEADS_FILE):
        with open(LEADS_FILE, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                print(" | ".join(row))
    print("\n")

if __name__ == "__main__":
    init_db()
    company = input("اسم الشركة: ")
    email = input("البريد الإلكتروني للشركة: ")
    if company and email:
        add_lead(company, email)
    show_leads()
