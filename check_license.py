import os
import re
import datetime
import subprocess

def get_license_file():
    """Vérifie si le fichier de licence est dans le répertoire courant ou dans le répertoire parent."""
    current_dir = os.getcwd()
    parent_dir = os.path.dirname(current_dir)

    license_file = os.path.join(current_dir, 'python.txt')
    if not os.path.exists(license_file):
        license_file = os.path.join(parent_dir, 'python.txt')

    if os.path.exists(license_file):
        print(f"Fichier de licence trouvé : {license_file}")
        return license_file
    print("Erreur : Fichier de licence introuvable.")
    return None

def parse_license(license_str):
    """Extrait les parties importantes de la licence et les valide."""
    print(f"Tentative d'analyse de la licence : {license_str}")
    
    # Vérification du format de la licence avec regex
    match = re.match(r'^(A1a9)(\d{3})([A-Z0-9]+):([A-F0-9-]{14})(\d{12})(\w+)$', license_str)
    if match:
        prefix = match.group(1)
        validity_days = int(match.group(2))
        serial_number = match.group(3)
        mac_address = match.group(4)
        date_str = match.group(5)
        user_identifier = match.group(6)

        # Extraire les parties de la date
        hours = int(date_str[:2])
        minutes = int(date_str[2:4])
        day = int(date_str[4:6])
        month = int(date_str[6:8])
        year = int(date_str[8:12])

        # Validation des valeurs de date
        try:
            license_date = datetime.datetime(year, month, day, hours, minutes)
        except ValueError as e:
            print(f"Erreur : Date de licence invalide. Détails : {e}")
            return None, None, None, None, None, None

        return validity_days, prefix, serial_number, mac_address, license_date, user_identifier
    
    print("Erreur : Format de licence invalide.")
    return None, None, None, None, None, None

def get_serial_number():
    """Essaie de récupérer le numéro de série via différentes méthodes."""
    serial_number = None
    try:
        serial_number = os.popen("wmic bios get serialnumber").read().strip().split("\n")[1].strip()
    except IndexError:
        pass

    if serial_number and "To be filled by O.E.M." not in serial_number:
        return serial_number

    try:
        serial_number = subprocess.check_output(
            ["powershell", "(Get-WmiObject win32_bios).SerialNumber"],
            universal_newlines=True
        ).strip()
    except subprocess.CalledProcessError as e:
        print(f"Erreur : Impossible de récupérer le numéro de série avec PowerShell. Détails : {e}")
    
    return serial_number if serial_number and "To be filled by O.E.M." not in serial_number else None

def get_mac_address():
    """Récupère l'adresse MAC de la machine."""
    try:
        mac_address = os.popen("getmac").read().splitlines()[0].split()[0]
        return mac_address.upper()
    except Exception as e:
        print(f"Erreur : Impossible de récupérer l'adresse MAC. Détails : {e}")
        return None

def check_mac_address(license_mac):
    """Vérifie si l'adresse MAC correspond à celle du client."""
    client_mac = get_mac_address()
    if not client_mac:
        print("Erreur : Impossible de récupérer l'adresse MAC de l'ordinateur.")
        return False
    return client_mac == license_mac

def check_serial_number(license_serial):
    """Vérifie si le numéro de série de l'ordinateur correspond à celui de la licence."""
    serial_number = get_serial_number()
    if serial_number is None:
        return license_serial == "To be filled by O.E.M."  # Accepter valeur par défaut

    return serial_number == license_serial

def is_license_valid():
    """Vérifie si la licence est valide."""
    license_file = get_license_file()
    if not license_file:
        return False

    try:
        with open(license_file, 'r') as f:
            license_content = f.read().strip()
    except IOError as e:
        print(f"Erreur : Impossible de lire le fichier de licence. Détails : {e}")
        return False

    validity_days, prefix, license_serial, license_mac, license_date, user_identifier = parse_license(license_content)
    
    if validity_days is None or prefix != 'A1a9' or license_mac is None or license_date is None:
        print("Erreur : Licence invalide ou préfixe incorrect.")
        return False

    current_time = datetime.datetime.now()
    expiration_date = license_date + datetime.timedelta(days=validity_days)

    if current_time > expiration_date:
        print(f"Erreur : La licence a expiré le {expiration_date.strftime('%Y-%m-%d %H:%M:%S')}.")
        return False

    if not check_serial_number(license_serial):
        print("Erreur : Le numéro de série ne correspond pas.")
        if license_serial != "To be filled by O.E.M.":
            return False

    if not check_mac_address(license_mac):
        print("Erreur : L'adresse MAC ne correspond pas.")
        return False

    print(f"Licence valide jusqu'au {expiration_date.strftime('%Y-%m-%d %H:%M:%S')}. Nom d'utilisateur : {user_identifier}.")
    return True

# Appel de la fonction pour vérifier la validité de la licence
if __name__ == "__main__":
    if is_license_valid():
        print("Licence est valide.")
    else:
        print("Licence est invalide ou expirée. Fermeture de l'application.")
