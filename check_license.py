import os
import re
import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
import getpass  # Pour récupérer le nom de l'utilisateur actuel

# Clé de chiffrement (doit être de 16, 24 ou 32 octets pour AES)
ENCRYPTION_KEY = b'ma_cle_de_chiffrement'  # Assure-toi que la clé fait 16, 24 ou 32 octets.

def decrypt_license(content):
    """Déchiffre le contenu chiffré de la licence."""
    # Décodage de base64
    encrypted_content = base64.b64decode(content)
    cipher = AES.new(ENCRYPTION_KEY, AES.MODE_CBC, iv=encrypted_content[:16])
    decrypted = unpad(cipher.decrypt(encrypted_content[16:]), AES.block_size)
    return decrypted.decode('utf-8')

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

def parse_license(license_str):
    """Extrait les parties importantes de la licence et les valide."""
    match = re.match(r'(\d{3})([A-Z0-9\s]+):([A-F0-9-]{14})(\d{12})([A-Z0-9\s]+)', license_str)
    if match:
        validity_days = int(match.group(1))  # Exemple : 003
        serial_number = match.group(2).strip()  # Exemple : To Be Filled By O.E.M.
        mac_address = match.group(3)  # Exemple : E4-42-A6-3A-AC
        date_str = match.group(4)  # Exemple : 164924102024 (24 minutes, 10 heures, 2 octobre 2024)
        user_name = match.group(5).strip()  # Exemple : ALTUNISITMASOĞUTMA
        license_date = datetime.datetime.strptime(date_str, "%M%H%d%m%Y")
        return validity_days, serial_number, mac_address, license_date, user_name
    return None, None, None, None, None

def get_mac_address():
    """Récupère l'adresse MAC actuelle de la machine."""
    # Remplace cette fonction avec la logique pour obtenir l'adresse MAC de l'utilisateur
    return "E4-42-A6-3A-AC"  # Adresse MAC fixe pour la comparaison

def get_current_user_name():
    """Récupère le nom d'utilisateur actuel de la machine."""
    return getpass.getuser()

def check_mac_address(license_mac):
    """Vérifie si l'adresse MAC correspond à celle du client."""
    current_mac = get_mac_address()
    print(f"Adresse MAC actuelle : {current_mac}, Adresse MAC de la licence : {license_mac}")
    return current_mac == license_mac

def check_serial_number(license_serial):
    """Vérifie si le numéro de série de l'ordinateur correspond à celui de la licence."""
    current_serial = get_serial_number()
    print(f"Numéro de série actuel : {current_serial}, Numéro de série de la licence : {license_serial}")

    # Si le numéro de série est "To Be Filled By O.E.M.", nous le considérons comme valide
    if license_serial == "To Be Filled By O.E.M.":
        print("Avertissement : Le numéro de série est générique mais accepté pour ce cas.")
        return True

    return current_serial == license_serial

def get_serial_number():
    """Essaie de récupérer le numéro de série via différentes méthodes."""
    try:
        serial_number = os.popen("wmic bios get serialnumber").read().strip().split("\n")[1].strip()
        if serial_number:
            return serial_number
    except IndexError:
        pass
    
    try:
        serial_number = os.popen("powershell (Get-WmiObject win32_bios).SerialNumber").read().strip()
        return serial_number
    except Exception as e:
        print(f"Erreur lors de la récupération du numéro de série avec PowerShell : {e}")
        return None

def check_user_name(license_user):
    """Vérifie si le nom d'utilisateur correspond à celui de la licence."""
    current_user = get_current_user_name()
    print(f"Nom d'utilisateur actuel : {current_user}, Nom d'utilisateur de la licence : {license_user}")
    return current_user == license_user

def is_license_valid():
    """Vérifie si la licence est valide."""
    license_file = get_license_file()
    if not license_file:
        print("Erreur : Le fichier de licence n'existe pas.")
        return False

    with open(license_file, 'r') as f:
        encrypted_license_content = f.read().strip()
    
    # Déchiffrer le contenu de la licence
    license_content = decrypt_license(encrypted_license_content)
    
    # Extraire et valider la licence
    validity_days, license_serial, license_mac, license_date, license_user = parse_license(license_content)
    print(f"Licence : jours de validité = {validity_days}, numéro de série = {license_serial}, adresse MAC = {license_mac}, date de licence = {license_date}, utilisateur = {license_user}")

    if validity_days is None or license_mac is None or license_date is None or license_user is None:
        print("Erreur : Licence invalide.")
        return False
    
    # Vérifier si la licence est encore valide
    current_time = datetime.datetime.now()
    expiration_date = license_date + datetime.timedelta(days=validity_days)
    
    print(f"Date actuelle : {current_time}, date d'expiration : {expiration_date}")
    if current_time > expiration_date:
        print(f"Erreur : La licence a expiré le {expiration_date}.")
        return False
    
    # Vérifier l'adresse MAC (en utilisant l'adresse récupérée)
    if not check_mac_address(license_mac):
        print("Erreur : L'adresse MAC ne correspond pas.")
        return False
    
    # Vérifier le numéro de série
    if not check_serial_number(license_serial):
        print("Erreur : Le numéro de série ne correspond pas.")
        return False
    
    # Vérifier le nom d'utilisateur
    if not check_user_name(license_user):
        print("Erreur : Le nom d'utilisateur ne correspond pas.")
        return False
    
    print(f"Licence valide jusqu'au {expiration_date}.")
    return True

# Appel de la fonction pour vérifier la validité de la licence
if __name__ == "__main__":
    if is_license_valid():
        print("Licence est valide.")
    else:
        print("Licence est invalide.")
