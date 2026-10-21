import smtplib
from email.mime.text import MIMEText

def send_b2b_offer(target_email, company_name):
    msg = MIMEText(f"Bonjour, nous proposons des solutions sur-mesure pour {company_name} via Adastra Web Service...")
    msg['Subject'] = f"Opportunité de partenariat avec {company_name}"
    msg['From'] = "votre_email@gmail.com"
    msg['To'] = target_email

    # قم بضبط إعدادات سيرفر الإرسال هنا
    print(f"Message envoyé à {company_name} ({target_email})")

# تجربة
# send_b2b_offer("client@enterprise.com", "Big Corp")


