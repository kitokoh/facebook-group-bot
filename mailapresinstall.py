import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Fonction pour envoyer l'e-mail
def send_email(client_email, sender_password, subject, message_body):
    # Informations sur le compte e-mail expéditeur
    sender_email = "info@turknovatech.com"

    # Configuration du serveur SMTP
    smtp_server = "mail.turknovatech.com"
    smtp_port = 587

    # Configuration de l'e-mail
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = client_email
    msg['Subject'] = subject

    # Ajouter le corps de l'e-mail
    msg.attach(MIMEText(message_body, 'plain'))

    # Envoyer l'e-mail via SMTP
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
                    # Extraire l'adresse e-mail après "Email: "
                    email = line.split("Email:")[1].strip()
                    return email
    except FileNotFoundError:
        print("Erreur : Le fichier info.txt n'a pas été trouvé.")
        return None

# Fonction pour lire le mot de passe de l'expéditeur depuis mail.txt dans le répertoire courant
def get_sender_password():
    try:
        # Récupérer le répertoire courant d'exécution
        current_dir = os.getcwd()
        mail_file_path = os.path.join(current_dir, 'mail.txt')
        
        with open(mail_file_path, 'r') as file:
            # Lire la première ligne contenant le mot de passe
            password = file.readline().strip()
            return password
    except FileNotFoundError:
        print(f"Erreur : Le fichier mail.txt n'a pas été trouvé dans {current_dir}.")
        return None

# Exemple d'utilisation
if __name__ == "__main__":
    client_email = get_client_email()  # Lire l'e-mail du destinataire depuis info.txt
    sender_password = get_sender_password()  # Lire le mot de passe depuis mail.txt dans le répertoire courant

    if client_email and sender_password:
        subject = "Votre sujet ici"
        message_body = "Bonjour, voici le contenu de votre e-mail."

        # Appel de la fonction pour envoyer l'e-mail
        send_email(client_email, sender_password, subject, message_body)
    else:
        print("Aucune adresse e-mail ou mot de passe valide trouvée.")
