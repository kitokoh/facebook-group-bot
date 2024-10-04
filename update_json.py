import os
import json

# Obtenir le nom d'utilisateur actuel
username = os.getlogin()

# Chemin du fichier data.json
json_file_path = 'data.json'

# Charger les données JSON
with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Remplacer "C:\\Users\\abdul\\" par "C:\\Users\\{username}\\"
for post in data['posts']:
    post['image'] = post['image'].replace("C:\\Users\\abdul\\", f"C:\\Users\\{username}\\")

# Sauvegarder les modifications dans data.json
with open(json_file_path, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print(f"Fichier JSON mis à jour avec le nom d'utilisateur : {username}")
