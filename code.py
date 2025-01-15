import json
import fonction_conf_address

def modig_config(line):

        # Liste pour stocker les lignes modifiées
        updated_lines = []

        # Récupérer le router-id à partir des données JSON
        router_id = router_data.get("router_id")

        # Parcourir chaque ligne et appliquer les modifications
        for line in lines:
            if line.startswith("hostname"):  # Modifier le hostname
                updated_lines.append("hostname {router_name}\n")
            elif line.startswith("interface Loopback"):  # Modifier l'interface Loopback'
                updated_lines.append("interface Loopback{router_name}\n")
            elif line.startswith("ipv6 address"):  # Modifier l'interface Loopback'
                updated_lines.append("ipv6 address {fonction_conf_address.conf_address(router_name)}\n")
            elif line.startswith("FastEthernet0/0"):  # Modifier le router bgp
                #Elimine les 4 lignes suivantes
                
                if #il y a pas cette interface:
                    updated_lines.append(" no ip address\n shutdown\n negotiation auto\n")
                else:
                    #ajouter l'addresse ipv6
                if ebgp:
                    #.....
                else:
                    #
                if rip:
                    updated_lines.append("ipv6 rip ng enable\n")
                if ospf:
                    updated_lines.append("ipv6 ospf 1 area 0\n")
                
            elif line.startswith("router bgp"):  # Modifier le router bgp
                updated_lines.append("router bgp {as_name}\n")
            elif line.startswith("bgp router-id"):  # Modifier le router bgp
                updated_lines.append("bgp router-id {router_id}\n")
            else:
                updated_lines.append(line)  # Conserver les lignes inchangées

        # Écrire les modifications dans le fichier
        with open('model_RIP_startup-config.cfg', 'w') as file:
            file.writelines(updated_lines)

    

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

        modig_config(lines)

        print("Modifications du fichier de configuration de {routeur_name} terminées.")
 
 # type: ignore
