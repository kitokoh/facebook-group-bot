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
    match = re.match(r'(\d{3})(A1a9)([A-Z0-9]+|To be filled by O.E.M.):([A-F0-9-]{14})(\d{12})', license_str)
    if match:
        validity_days = int(match.group(1))
        prefix = match.group(2)
        serial_number = match.group(3)
        mac_address = match.group(4)
        date_str = match.group(5)
        
        # Extraire les parties de la date
        hours = int(date_str[:2])  # 15 heures
        minutes = int(date_str[2:4])  # 11 minutes
        day = int(date_str[4:6])  # 25
        month = int(date_str[6:8])  # 10 (octobre)
        year = int(date_str[8:12])  # 2024

        # Créer l'objet datetime avec les valeurs extraites
        license_date = datetime.datetime(year, month, day, hours, minutes)

        user_identifier = date_str[12:]  # 212 (nom d'utilisateur)
        
        return validity_days, prefix, serial_number, mac_address, license_date, user_identifier
    return None, None, None, None, None, None

def get_serial_number():
    """Essaie de récupérer le numéro de série via différentes méthodes."""
    serial_number = None
    try:
        serial_number = os.popen("wmic bios get serialnumber").read().strip().split("\n")[1].strip()
    except Exception as e:
        print(f"Erreur lors de la récupération du numéro de série (WMIC) : {e}")

    if serial_number and "To be filled by O.E.M." not in serial_number:
        return serial_number

    try:
        serial_number = os.popen("powershell (Get-WmiObject win32_bios).SerialNumber").read().strip()
    except Exception as e:
        print(f"Erreur : Impossible de récupérer le numéro de série avec PowerShell : {e}")
    
    return serial_number if serial_number and "To be filled by O.E.M." not in serial_number else None

def check_mac_address(license_mac):
    """Vérifie si l'adresse MAC correspond à celle du client, en utilisant une adresse fixe."""
    fixed_mac = "E4-42-A6-3A-AC"  # Adresse MAC fixe
    return fixed_mac == license_mac

def check_serial_number(license_serial):
    """Vérifie si le numéro de série de l'ordinateur correspond à celui de la licence."""
    serial_number = get_serial_number()
    if serial_number is None:  # Si le numéro de série n'est pas récupéré
        return license_serial == "To be filled by O.E.M."  # Accepter si licence a une valeur par défaut
    return serial_number == license_serial

def display_error(message):
    """Affiche un message d'erreur."""
    print(f"Erreur : {message}")

def is_license_valid():
    """Vérifie si la licence est valide."""
    license_file = get_license_file()
    if not license_file:
        display_error("Le fichier de licence n'existe pas.")
        return False

    try:
        with open(license_file, 'r') as f:
            license_content = f.read().strip()
    except Exception as e:
        display_error(f"Impossible de lire le fichier de licence : {e}")
        return False
    
    validity_days, prefix, license_serial, license_mac, license_date, user_identifier = parse_license(license_content)
    
    if validity_days is None or prefix != 'A1a9' or license_mac is None or license_date is None:
        display_error("Licence invalide ou préfixe incorrect.")
        return False

    current_time = datetime.datetime.now()
    expiration_date = license_date + datetime.timedelta(days=validity_days)

    if current_time > expiration_date:
        display_error(f"La licence a expiré le {expiration_date}.")
        return False

    if not check_serial_number(license_serial):
        display_error("Le numéro de série ne correspond pas.")
        return False

    if not check_mac_address(license_mac):
        display_error("L'adresse MAC ne correspond pas.")
        return False

    print(f"Licence valide jusqu'au {expiration_date}. Nom d'utilisateur : {user_identifier}.")
    return True

# Appel de la fonction pour vérifier la validité de la licence
if __name__ == "__main__":
    if is_license_valid():
        print("Licence est valide.")
    else:
        print("Licence est invalide.")
