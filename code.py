import json

def modif_config(lines):




# Charger le fichier JSON
with open ("GNS.json", 'r') as json_file:
    data = json.load(json_file)

# Parcourir chaque AS dans le fichier JSON
for as_name, as_data in data.items():
    protocol = as_data.get("protocol", "unknown")  # Récupérer le protocole utilisé par l'AS
    routeurs = as_data.get("routeurs", {}) #Récupérer les routeurs présents dans chaque AS

    # Parcourir chaque routeur dans l'AS
    for router_name, router_data in routeurs.items():
        # Nom du fichier basé sur le nom du routeur
        filename = f"{router_name}_startup-config.cfg"


        # Lire le fichier existant et remplacer certaines informations
        with open('config.cfg', 'r') as file:
            lines = file.readlines()  # Lire toutes les lignes du fichier

        # Liste pour stocker les lignes modifiées
        updated_lines = []

        # Parcourir chaque ligne et appliquer les modifications
        for line in lines:
            if line.startswith("hostname"):  # Modifier le hostname
                updated_lines.append("hostname {router_name}\n")
            elif line.startswith("protocol"):  # Modifier le protocole
                updated_lines.append("protocol {protocol}\n")
            else:
                updated_lines.append(line)  # Conserver les lignes inchangées

        # Écrire les modifications dans le fichier
        with open('config.cfg', 'w') as file:
            file.writelines(updated_lines)

        print(f"Modifications du fichier de configuration du routeur {router_name} terminées.")
 
 
 
 
 # type: ignore