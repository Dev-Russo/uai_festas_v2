import os
import smtplib
from email.message import EmailMessage

SMTP_HOST = os.environ.get("SMTP_HOST")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
FROM_ADDRESS = os.environ.get("EMAIL_FROM", SMTP_USER)


def send_email_with_attachment(to_email: str, subject: str, body: str, attachment_bytes: bytes, filename: str):
    if not SMTP_HOST or not SMTP_USER:
        # Fallback: write file to /tmp and log
        path = f"/tmp/{filename}"
        with open(path, "wb") as f:
            f.write(attachment_bytes)
        print(f"SMTP not configured. Ticket saved to {path}. Email to {to_email} not sent.")
        return

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = FROM_ADDRESS
    msg["To"] = to_email
    msg.set_content(body or "")

    msg.add_attachment(attachment_bytes, maintype="application", subtype="pdf", filename=filename)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
        s.starttls()
        s.login(SMTP_USER, SMTP_PASSWORD)
        s.send_message(msg)
