import json
import fonction_conf_address

def modif_config_policies(lines, dico, nAS, routeur, filename):
    updated_lines = []
    # Communities sous la forme AS:NBR
    communities = {"customer" : f"{nAS}:300", "peer": f"{nAS}:150", "provider" : f"{nAS}:100"}
    
    liens_bgp = dico["Border"]["Liens_border"]

    interfaces_bordures = fonction_conf_address.border(dico["Border"])

    # On regarde si routeur connecté à client, peer ou provider
    co_customer = False
    co_peer = False
    co_provider = False

    clients = dico["AS"][nAS]["AS_voisins"]["customers"]
    peers = dico["AS"][nAS]["AS_voisins"]["peers"]
    providers = dico["AS"][nAS]["AS_voisins"]["providers"]

    # On détermine si le routeur est un routeur de bordure et son voisin BGP
    for lien in liens_bgp :
        if routeur in lien :
            if lien[0] == routeur :
                voisin_bgp = lien[1]
            if lien[1] == routeur :
                voisin_bgp = lien[0]
        #else : # Si le routeur n'est pas un routeur de bordure on n'applique pas tout le reste
         #   return
    
    # On détermine si le routeur est connecté à un routeur d'un client, d'un provider ou d'un peer
    AS_voisin = voisin_bgp[1] + "0"
    if AS_voisin in clients :
        co_customer = True
    if AS_voisin in peers :
        co_peer = True
    if AS_voisin in providers :
        co_provider = True

    #for AS in dico["AS"].keys():
        # On regarde quel est le lien entre l'AS qu'on configure et l'AS voisin
        #if AS == AS_voisin :
         #   if AS in clients :
          #      co_customer = True
           # if AS in peers :
            #    co_peer = True 
            #if AS in providers :
             #   co_provider = True 

    print(f"Routeur:{routeur}, co_fournisseur:{co_provider}, co_client:{co_customer}, co_peer:{co_peer}")
    updates_lines = []

    for line in lines :
        if line.startswith("  neighbor"):
            updated_lines.append(line) # On conserve la ligne qui active le voisin bgp.
            if co_customer :
                if line.startswith(f"  neighbor {interfaces_bordures[voisin_bgp]["GigabitEthernet3/0"][0:-3]}"):
                    updated_lines.append(f"{line[:-9]}send-community both\n"+f"{line[:-9]}route-map TAG_CLIENT in\n")
                else :    
                    updated_lines.append(f"{line[:-9]}send-community both\n")
            elif co_peer :
                if line.startswith(f"  neighbor {interfaces_bordures[voisin_bgp]["GigabitEthernet3/0"][0:-3]}"):
                    updated_lines.append(f"{line[:-9]}route-map TAG_peer in\n")
                    updated_lines.append(f"{line[:-9]}route-map filtre_client out\n")
            elif co_provider :
                if line.startswith(f"  neighbor {interfaces_bordures[voisin_bgp]["GigabitEthernet3/0"][0:-3]}"):
                    updated_lines.append(f"{line[:-9]}route-map TAG_provider in\n")
                    updated_lines.append(f"{line[:-9]}route-map filtre_client out\n")

        elif line.startswith("ip forward-protocol nd"): 
            updated_lines.append("ip forward-protocol nd\n!\nip bgp-community new-format\n")
            if co_peer or co_provider :
                updated_lines.append(f"ip community-list standard com_client permit {communities["customer"]}\n") # On tag toutes les routes qui viennent d'un client.

        elif line.startswith(" redistribute connected"): 
            updated_lines.append(" redistribute connected\n!\n!\nipv6 router rip enable\n!\n!\n")
            if co_customer:
                updated_lines.append(f"route-map TAG_client permit 10 \n set local-preference 150 \n")
                updated_lines.append(f" set community {communities["customer"]} additive \n")
                updated_lines.append(f"route-map TAG_client permit 50 \n")

            elif co_peer:
                updated_lines.append(f"route-map TAG_peer permit 10 \n set local-preference 100 \n!\nroute-map TAG_peer permit 50\n!\n")
                updated_lines.append(f"route-map filtre_client permit 10 \n match community com_client\n!\nroute-map filtre_client deny 50")

            elif co_provider:
                updated_lines.append(f"route-map TAG_provider permit 10 \n set local-preference 50 \n!\nroute-map TAG_provider permit 50\n!\n")
                updated_lines.append(f"route-map filtre_client permit 10 \n match community com_client\n!\nroute-map filtre_client deny 50\n")
        
        elif line.startswith("ipv6 router ospf 1"): 
            updated_lines.append(line)
            if co_customer:
                updated_lines.append(f"route-map TAG_client permit 10 \n set local preference 150 \n")
                updated_lines.append(f" set community {communities["customer"]} additive \n")
                updated_lines.append(f"route-map TAG_client permit 50 \n")

            elif co_peer:
                updated_lines.append(f"route-map TAG_peer permit 10 \n set local preference 100 \n!\n\nroute-map TAG_peer permit 50\n!\n")
                updated_lines.append(f"route-map filtre_client permit 10 \n match community com_client\n!\n\nroute-map filtre_client deny 50\n")

            elif co_provider:
                updated_lines.append(f"route-map TAG_provider permit 10 \n set local preference 50 \n!\n\nroute-map TAG_provider permit 50\n!\n")
                updated_lines.append(f"route-map filtre_client permit 10 \n match community com_client\n!\n\nroute-map filtre_client deny 50\n")
        
        else:
            updated_lines.append(line)  # Conserver les lignes inchangées


    # Écrire les modifications dans le fichier
    with open(filename, 'w') as file: # Ce fichier n'existe pas encore, il est donc créé.
        file.writelines(updated_lines)
        print(f"Ajout des policies sur le fichier de configuration de {routeur} terminées.")

    



    

    

    
