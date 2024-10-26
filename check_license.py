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
    
    # Regex assouplie pour accepter les valeurs comme 'To be filled by O.E.M.'
    match = re.match(r'^(A1a9)(\d{3})([A-Z0-9 ]+):([A-F0-9-]{14})(\d{12})(\w+)$', license_str)
    if match:
        prefix = match.group(1)
        validity_days = int(match.group(2))
        serial_number = match.group(3).strip()
        mac_address = match.group(4)
        date_str = match.group(5)
        user_identifier = match.group(6)

        print(f"Analyse réussie : Préfixe: {prefix}, Validité: {validity_days}, Numéro de série: {serial_number}, MAC: {mac_address}, Date: {date_str}, Utilisateur: {user_identifier}")

        # Extraire les parties de la date
        try:
            hours = int(date_str[:2])
            minutes = int(date_str[2:4])
            day = int(date_str[4:6])
            month = int(date_str[6:8])
            year = int(date_str[8:12])
            license_date = datetime.datetime(year, month, day, hours, minutes)
            print(f"Date extraite : {license_date}")
        except ValueError as e:
            print(f"Erreur : Date de licence invalide. Détails : {e}")
            return None, None, None, None, None, None

        return validity_days, prefix, serial_number, mac_address, license_date, user_identifier
    print("Erreur : Format de licence invalide. Format attendu: A1a9<valeurs>:<MAC>:<date>:<utilisateur>")
    return None, None, None, None, None, None

def get_serial_number():
    """Essaie de récupérer le numéro de série via différentes méthodes."""
    serial_number = None
    try:
        serial_number = os.popen("wmic bios get serialnumber").read().strip().split("\n")[1].strip()
        print(f"Numéro de série récupéré via wmic : {serial_number}")
    except IndexError:
        print("Erreur : Numéro de série introuvable via wmic.")
    
    if serial_number and "To be filled by O.E.M." not in serial_number:
        return serial_number

    try:
        serial_number = subprocess.check_output(
            ["powershell", "(Get-WmiObject win32_bios).SerialNumber"],
            universal_newlines=True
        ).strip()
        print(f"Numéro de série récupéré via PowerShell : {serial_number}")
    except subprocess.CalledProcessError as e:
        print(f"Erreur : Impossible de récupérer le numéro de série avec PowerShell. Détails : {e}")
    
    if serial_number and "To be filled by O.E.M." not in serial_number:
        return serial_number

    return "To be filled by O.E.M."  # Valeur par défaut si rien n'est récupéré

def check_mac_address(license_mac):
    """Vérifie si l'adresse MAC correspond à l'adresse MAC fixe."""
    fixed_mac_address = "E4-42-A6-3A-AC"
    mac_valid = license_mac == fixed_mac_address
    print(f"Vérification de l'adresse MAC : Licence MAC = {license_mac}, Fixe MAC = {fixed_mac_address}, Résultat = {mac_valid}")
    return mac_valid

def check_serial_number(license_serial):
    """Vérifie si le numéro de série de l'ordinateur correspond à celui de la licence."""
    serial_number = get_serial_number()
    print(f"Vérification du numéro de série : Licence Serial = {license_serial}, Ordinateur Serial = {serial_number}")
    if serial_number == "To be filled by O.E.M.":
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
