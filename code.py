import json

# Charger le fichier JSON
with open ("GNS.json", 'r') as json_file:
    data = json.load(json_file)

for i in range(1,14):
    # Ouvrir un fichier pour écrire la configuration
    with open('config.cfg', 'w') as cfg_file:
        cfg_file.write(f"hostname {data.get('hostname', 'R22')}\n")

