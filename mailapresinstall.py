import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys  # Pour récupérer les arguments de la ligne de commande

# Fonction pour envoyer l'e-mail
def send_email(client_email, sender_password, subject, message_body):
    sender_email = "info@turknovatech.com"
    smtp_server = "mail.turknovatech.com"
    smtp_port = 587

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = client_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message_body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, client_email, msg.as_string())
        server.quit()
        print("E-mail envoyé avec succès à", client_email)
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'e-mail: {e}")

# Fonction pour lire l'adresse e-mail depuis le fichier info.txt
def get_client_email():
    try:
        with open(r'C:\bon\info.txt', 'r') as file:
            for line in file:
                if line.startswith("Email:"):
                    email = line.split("Email:")[1].strip()
                    return email
    except FileNotFoundError:
        print("Erreur : Le fichier info.txt n'a pas été trouvé.")
        return None

# Exemple d'utilisation
if __name__ == "__main__":
    client_email = get_client_email()

    # Récupérer le mot de passe transmis en argument depuis le script batch
    if len(sys.argv) > 1:
        sender_password = sys.argv[1]
    else:
        sender_password = None

    if client_email and sender_password:
        subject = "Votre sujet ici"
        message_body = "Bonjour, voici le contenu de votre e-mail."
        send_email(client_email, sender_password, subject, message_body)
    else:
        print("Aucune adresse e-mail ou mot de passe valide trouvée.")
