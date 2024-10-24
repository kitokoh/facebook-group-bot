import os
import re
import datetime
import uuid
import hashlib
from cryptography.fernet import Fernet

# Générer et stocker une clé de chiffrement pour la licence (exécuté une seule fois lors du déploiement)
def generate_key():
    return Fernet.generate_key()

# Fonction pour charger ou générer une clé de chiffrement
def load_key():
    # Chemin de la clé
    key_file = 'license_key.key'
    if not os.path.exists(key_file):
        # Générer une nouvelle clé
        key = generate_key()
        with open(key_file, 'wb') as f:
            f.write(key)
    else:
        # Charger la clé existante
        with open(key_file, 'rb') as f:
            key = f.read()
    return key

# Chiffrement de la licence
def encrypt_license(license_data, key):
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(license_data.encode())
    return encrypted_data

# Déchiffrement de la licence
def decrypt_license(encrypted_data, key):
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data).decode()
    return decrypted_data

# Génération du fichier de licence avec chiffrement
def create_license(validity_days, serial_number, mac_address, license_date):
    # Création de la chaîne de licence
    date_str = license_date.strftime("%H%M%d%m%Y")  # Format : HHMMDDMMYYYY
    license_str = f"{validity_days:03d}{serial_number}:{mac_address}{date_str}"
    
    # Chiffrement
    key = load_key()
    encrypted_license = encrypt_license(license_str, key)
    
    # Écriture dans un fichier
    with open('python.txt', 'wb') as f:
        f.write(encrypted_license)

# Récupérer l'adresse MAC
def get_mac_address():
    mac = uuid.getnode()
    mac_str = ':'.join(re.findall('..', f'{mac:012x}')).upper()
    return mac_str

# Récupérer le numéro de série (en excluant les cas génériques comme "To Be Filled By O.E.M.")
def get_serial_number():
    try:
        serial_number = os.popen("wmic bios get serialnumber").read().strip().split("\n")[1].strip()
        if serial_number and serial_number != "To Be Filled By O.E.M.":
            return serial_number
    except IndexError:
        pass
    
    return None

# Parser la licence chiffrée
def parse_license(encrypted_license, key):
    try:
        license_str = decrypt_license(encrypted_license, key)
        match = re.match(r'(\d{3})([A-Z0-9]+):([A-F0-9-:]+)(\d{12})', license_str)
        if match:
            validity_days = int(match.group(1))
            serial_number = match.group(2)
            mac_address = match.group(3)
            date_str = match.group(4)
            license_date = datetime.datetime.strptime(date_str, "%H%M%d%m%Y")
            return validity_days, serial_number, mac_address, license_date
    except Exception as e:
        print(f"Erreur lors du déchiffrement : {e}")
    
    return None, None, None, None

# Vérification de la validité de la licence
def is_license_valid():
    # Charger la clé de chiffrement
    key = load_key()

    # Vérifier si le fichier de licence existe
    license_file = get_license_file()
    if not license_file:
        print("Erreur : Le fichier de licence n'existe pas.")
        return False

    # Lire la licence chiffrée
    with open(license_file, 'rb') as f:
        encrypted_license = f.read()

    # Extraire les informations de la licence
    validity_days, license_serial, license_mac, license_date = parse_license(encrypted_license, key)
    if None in [validity_days, license_serial, license_mac, license_date]:
        print("Erreur : Licence invalide.")
        return False

    # Vérifier la validité dans le temps
    current_time = datetime.datetime.now()
    expiration_date = license_date + datetime.timedelta(days=validity_days)
    if current_time > expiration_date:
        print(f"Erreur : La licence a expiré le {expiration_date}.")
        return False

    # Vérifier le numéro de série s'il est disponible et valide
    system_serial = get_serial_number()
    if system_serial:
        print(f"Numéro de série actuel : {system_serial}, Numéro de licence : {license_serial}")
        if system_serial != license_serial:
            print("Erreur : Le numéro de série ne correspond pas.")
            return False
    else:
        print("Aucun numéro de série valide détecté sur le système.")

    # Vérifier l'adresse MAC
    system_mac = get_mac_address()
    print(f"Adresse MAC actuelle : {system_mac}, Adresse MAC de la licence : {license_mac}")
    if system_mac != license_mac:
        print("Erreur : L'adresse MAC ne correspond pas.")
        return False

    print(f"Licence valide jusqu'au {expiration_date}.")
    return True

# Récupération du fichier de licence (déjà existant ou non)
def get_license_file():
    """Vérifie si le fichier de licence est dans le répertoire courant ou dans le répertoire au-dessus."""
    current_dir = os.getcwd()
    parent_dir = os.path.dirname(current_dir)
    
    license_file = os.path.join(current_dir, 'python.txt')
    if not os.path.exists(license_file):
        license_file = os.path.join(parent_dir, 'python.txt')
    
    if os.path.exists(license_file):
        return license_file
    return None

# Exemple de création d'une licence
if __name__ == "__main__":
    validity_days = 365  # Licence annuelle
    serial_number = get_serial_number() or "UNKNOWN_SERIAL"
    mac_address = get_mac_address()
    license_date = datetime.datetime.now()

    # Générer la licence
    create_license(validity_days, serial_number, mac_address, license_date)

    # Vérifier la licence
    is_license_valid()
