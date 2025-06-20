# Phase 1.3 – The Final Cinematic Version of `email_sender.py`

import smtplib
import csv
import os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import time
import logging

# === Load .env credentials === #
load_dotenv()

EMAIL_ACCOUNTS = [
    {"email": os.getenv("EMAIL_1"), "password": os.getenv("PASS_1"), "smtp": "smtp.zoho.com", "port": 587},
    {"email": os.getenv("EMAIL_2"), "password": os.getenv("PASS_2"), "smtp": "smtp.zoho.com", "port": 587},
    {"email": os.getenv("EMAIL_3"), "password": os.getenv("PASS_3"), "smtp": "smtp.zoho.com", "port": 587},
    {"email": os.getenv("EMAIL_4"), "password": os.getenv("PASS_4"), "smtp": "smtp.zoho.com", "port": 587}
]

CONTACTS_FILE = "contacts.csv"
LOG_FILE = "email_log.txt"
FROM_NAME = "Arthur Dixon for Congress"

# === Dynamic Email Templates === #
HTML_TEMPLATE = """
<html>
  <body style="font-family: sans-serif; font-size: 16px; color: #222;">
    <p>Dear {name},</p>
    <p>We’re building something powerful in the heart of Los Angeles. A campaign rooted in justice, dignity, and a future that belongs to us all.</p>
    <p>Arthur Dixon is not just another candidate — he’s a survivor, a fighter, and a visionary.</p>
    <p>Our movement is rising. And we want you in it.</p>
    <p><a href='https://arthurdixonforcongress.com' style="background: #007BFF; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Donate Now →</a></p>
    <p>In Solidarity,<br><b>Arthur Dixon</b><br><i>The People’s Candidate</i></p>
  </body>
</html>
"""

PLAIN_TEMPLATE = """
Dear {name},

We’re building something powerful in the heart of Los Angeles. A campaign rooted in justice, dignity, and a future that belongs to us all.

Arthur Dixon is not just another candidate — he’s a survivor, a fighter, and a visionary.

Our movement is rising. And we want you in it.

Join us and donate now → https://arthurdixonforcongress.com

In Solidarity,
Arthur Dixon
The People’s Candidate
"""

# === Logging Setup === #
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')

# === Email Sending Logic === #
def send_email(smtp_info, recipient_email, recipient_name, subject, preheader):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{FROM_NAME} <{smtp_info['email']}>"
    msg["To"] = recipient_email

    html_body = HTML_TEMPLATE.format(name=recipient_name or "Friend")
    plain_body = PLAIN_TEMPLATE.format(name=recipient_name or "Friend")

    msg.attach(MIMEText(plain_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    try:
        server = smtplib.SMTP(smtp_info["smtp"], smtp_info["port"])
        server.starttls()
        server.login(smtp_info["email"], smtp_info["password"])
        server.sendmail(smtp_info["email"], recipient_email, msg.as_string())
        server.quit()
        logging.info(f"✅ Sent to {recipient_email} from {smtp_info['email']}")
    except Exception as e:
        logging.error(f"❌ Failed to send to {recipient_email}: {e}")

# === Contact Loader + Scheduler === #
def load_contacts(file_path):
    contacts = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            contacts.append({
                "email": row.get("email1"),
                "name": row.get("first_name", "Friend"),
                "send_time": row.get("send_time", "")
            })
    return contacts

def dispatch_emails(subject, preheader):
    contacts = load_contacts(CONTACTS_FILE)
    account_index = 0

    for contact in contacts:
        if contact["email"]:
            # Handle optional scheduling per contact
            if contact.get("send_time"):
                try:
                    send_dt = datetime.strptime(contact["send_time"], "%Y-%m-%d %H:%M:%S")
                    now = datetime.now()
                    delay = (send_dt - now).total_seconds()
                    if delay > 0:
                        logging.info(f"Scheduling email to {contact['email']} at {send_dt}")
                        time.sleep(delay)
                except Exception as e:
                    logging.warning(f"Invalid send_time for {contact['email']}: {e}")

            smtp_info = EMAIL_ACCOUNTS[account_index % len(EMAIL_ACCOUNTS)]
            send_email(smtp_info, contact["email"], contact["name"], subject, preheader)
            account_index += 1

if __name__ == "__main__":
    print("\U0001F680 Dispatching campaign emails... This could change history.")
    SUBJECT = input("Enter subject: ") or "🔥 Arthur Dixon Is Rising — Join the Movement"
    PREHEADER = input("Enter preheader: ") or "CA-34’s future starts now. This is your invitation."
    dispatch_emails(SUBJECT, PREHEADER)
    print(f"\U0001F4EC Done. Review logs in: {LOG_FILE}")
