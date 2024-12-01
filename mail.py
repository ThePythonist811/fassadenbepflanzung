import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from datetime import datetime

def send_mail(subject, body, recipients, attachments=None):
    print("Connecting to mail server...")
    # Gmail credentials
    sender_email = "fassadenbepflanzung3@gmail.com"
    sender_password = "yivv ljaq xlew lzdm"

    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ", ".join(recipients)
    msg['Subject'] = subject

    # Add body
    msg.attach(MIMEText(body, 'plain'))

    # Add attachments
    if attachments:
        for file_path in attachments:
            print(f"Attaching file: {file_path}")
            with open(file_path, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file_path))
                msg.attach(part)

    print("Attempting to send mail...")
    # Connect using SSL
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        print(f"Email sent successfully to {recipients}")

def send_plant_report():
    print("Starting send_plant_report...")
    
    # Define recipients
    recipients = [
        "cosmin.fiegen@web.de",
        "leo.kuehn@wieland-gymnasium.de",
        "martin.guldan@wieland-gymnasium.de"
    ]
    
    # Dynamically determine attachments (e.g., based on today's date)
    today = datetime.now().strftime("%Y-%m-%d")
    attachments = [
        f"{today}_sensor_comparison.png",
        f"sensordata/sensordata.db",
        f"{today}_sensordaten.xlsx"
    ]
    
    # Define subject and body
    subject = "Täglicher Pflanzenbericht"
    body = """
    Siehe Anhang
    """
    
    # Send email with dynamic attachments
    send_mail(subject, body, recipients, attachments)
