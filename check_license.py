import os
import re
import datetime

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
    match = re.match(r'(\d{3})(A1a9)([A-Z0-9]+):([A-F0-9-]{14})(\d{12})', license_str)
    if match:
        validity_days = int(match.group(1))  # Exemple : 003
        prefix = match.group(2)  # Préfixe attendu : A1a9
        serial_number = match.group(3)  # Exemple : H6N0CV02H127234
        mac_address = match.group(4)  # Exemple : E4-42-A6-3A-AC
        date_str = match.group(5)  # Exemple : 172302102024 (2 Octobre 2024, 17:23)
        license_date = datetime.datetime.strptime(date_str, "%H%M%d%m%Y")
        return validity_days, prefix, serial_number, mac_address, license_date
    return None, None, None, None, None

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
    except IndexError:
        print("Erreur : Impossible de récupérer le numéro de série avec PowerShell.")
        return None

def check_mac_address(license_mac):
    """Vérifie si l'adresse MAC correspond à celle du client, en utilisant une adresse fixe."""
    fixed_mac = "E4-42-A6-3A-AC"  # Adresse MAC fixe
    print(f"Adresse MAC fixe : {fixed_mac}, Adresse MAC de la licence : {license_mac}")
    return fixed_mac == license_mac

def check_serial_number(license_serial):
    """Vérifie si le numéro de série de l'ordinateur correspond à celui de la licence."""
    serial_number = get_serial_number()
    if serial_number:
        print(f"Numéro de série actuel : {serial_number}, Numéro de série de la licence : {license_serial}")
        return serial_number == license_serial
    else:
        print("Erreur : Impossible de récupérer le numéro de série.")
        return False

def is_license_valid():
    """Vérifie si la licence est valide."""
    license_file = get_license_file()
    if not license_file:
        print("Erreur : Le fichier de licence n'existe pas.")
        return False

    with open(license_file, 'r') as f:
        license_content = f.read().strip()
    
    # Extraire et valider la licence
    validity_days, prefix, license_serial, license_mac, license_date = parse_license(license_content)
    print(f"Licence : jours de validité = {validity_days}, préfixe = {prefix}, numéro de série = {license_serial}, adresse MAC = {license_mac}, date de licence = {license_date}")

    if validity_days is None or prefix != 'A1a9' or license_serial is None or license_mac is None or license_date is None:
        print("Erreur : Licence invalide ou préfixe incorrect.")
        return False
    
    # Vérifier si la licence est encore valide
    current_time = datetime.datetime.now()
    expiration_date = license_date + datetime.timedelta(days=validity_days)
    
    print(f"Date actuelle : {current_time}, date d'expiration : {expiration_date}")
    if current_time > expiration_date:
        print(f"Erreur : La licence a expiré le {expiration_date}.")
        return False
    
    # Vérifier le numéro de série de l'ordinateur
    if not check_serial_number(license_serial):
        print("Erreur : Le numéro de série ne correspond pas.")
        return False
    
    # Vérifier l'adresse MAC (en utilisant l'adresse fixe)
    if not check_mac_address(license_mac):
        print("Erreur : L'adresse MAC ne correspond pas.")
        return False
    
    print(f"Licence valide jusqu'au {expiration_date}.")
    return True

# Appel de la fonction pour vérifier la validité de la licence
if __name__ == "__main__":
    if is_license_valid():
        print("Licence est valide.")
    else:
        print("Licence est invalide.")
