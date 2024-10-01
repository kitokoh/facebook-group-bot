import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Retrieve the SMTP password from the environment variable
password = os.getenv('SMTP_PASSWORD')

# Other email parameters
from_addr = "info@turknovatech.com"
to_addr = "turk.novatech@gmail.com"
subject = "Journal d'installation"
body = "Veuillez trouver ci-joint le journal d'installation."

log_file_path = os.path.expanduser("~/Desktop/journalInstallation.txt")

msg = MIMEMultipart()
msg['From'] = from_addr
msg['To'] = to_addr
msg['Subject'] = subject
msg.attach(MIMEText(body, 'plain'))

with open(log_file_path, "rb") as attachment:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f"attachment; filename={os.path.basename(log_file_path)}")
    msg.attach(part)

smtp_server = "mail.turknovatech.com"
smtp_port = 587

try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()
    print("[OK] - Email envoyé avec succès !")
except Exception as e:
    print(f"[ERROR] - Échec de l'envoi de l'email: {e}")
