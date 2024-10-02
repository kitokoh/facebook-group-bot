from scraper import Scraper
from check_license import is_license_valid

# Vérification de la licence avant de démarrer
if is_license_valid():
    print("Licence valide. Démarrage du script principal...")
    scraper = Scraper()
    scraper.post_in_groups()
else:
    print("Licence invalide ou expirée. Fermeture de l'application.")
