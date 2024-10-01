import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

# Define email parameters
from_addr = "info@turknovatech.com"
to_addr = "turk.novatech@gmail.com"
subject = "Journal d'installation"
body = "Veuillez trouver ci-joint le journal d'installation."
password = "7LdXDMXLkQ7G"

# Define the path to the log file
log_file_path = os.path.expanduser("~/Desktop/journalInstallation.txt")

# Create the email message
msg = MIMEMultipart()
msg['From'] = from_addr
msg['To'] = to_addr
msg['Subject'] = subject

# Attach the body to the email
msg.attach(MIMEText(body, 'plain'))

# Attach the log file
with open(log_file_path, "rb") as attachment:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f"attachment; filename={os.path.basename(log_file_path)}")
    msg.attach(part)

# SMTP server configuration
smtp_server = "mail.turknovatech.com"
smtp_port = 587

# Send the email
try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Upgrade to TLS
    server.login(from_addr, password)
    text = msg.as_string()
    server.sendmail(from_addr, to_addr, text)
    server.quit()
    print("[OK] - Email envoyé avec succès !")
except Exception as e:
    print(f"[ERROR] - Échec de l'envoi de l'email: {e}")
