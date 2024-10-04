import sys
from scraper import Scraper

# Vérifie si un mot-clé est fourni en argument
if len(sys.argv) > 1:
    keyword = sys.argv[1]
else:
    print("Aucun mot-clé fourni.")
    sys.exit(1)

scraper = Scraper()
scraper.save_groups(keyword)
