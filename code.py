import json

# Charger le fichier JSON
with open ("GNS.json", 'r') as json_file:
    data = json.load(json_file)

# Parcourir chaque AS dans le fichier JSON
for as_name, as_data in data.items():
    protocol = as_data.get("protocol", "unknown")  # Récupérer le protocole utilisé par l'AS
    routeurs = as_data.get("routeurs", {}) #Récupérer les routeurs présents dans chaque AS
    interface_loopback = as_data.get("interface loopback")

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
            elif line.startswith("interface Loopback"):  # Modifier l'interface Loopback'
                updated_lines.append("interface Loopback{router_name}\n")
            elif line.startswith("ipv6 address"):  # Modifier l'interface Loopback'
                updated_lines.append("ipv6 address {addresse_a_modifier}\n")
            elif line.startswith("router bgp"):  # Modifier le router bgp
                updated_lines.append("router bgp {as_name}\n")
            else:
                updated_lines.append(line)  # Conserver les lignes inchangées

        # Ajouter les voisins
        voisins = router_data.get("voisins", [])
        if voisins:
            updated_lines.append("neighbors:\n")
            for voisin in voisins:
                updated_lines.append(f"  - {voisin}\n")

        # Écrire les modifications dans le fichier
        with open('config.cfg', 'w') as file:
            file.writelines(updated_lines)

        print("Modifications terminées.")
 # type: ignore