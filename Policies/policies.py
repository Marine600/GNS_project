import json


# On applique cette fonction à tous les routeurs de bordure de notre AS après leur avoir préalablement appliqué la fonction de configuration de base.
def modif_config_policies(lines, dico_policies, routeur, filename):

    nb_router = routeur[1]+routeur[2]
    
    # On détermine si le routeur est connecté à un client:
    co_client = False
    nb_neighbor_customer = 0
    for As in dico_policies["Client"].values():
        for lien_ebgp in dico_policies["Client"][As]["Liens_ebgp"]:
            if routeur in lien_ebgp:
                co_client = True
                if lien_ebgp[0] == routeur:
                    nb_neighbor_customer = lien_ebgp[1]
                else:
                    nb_neighbor_customer = lien_ebgp[0]
    
    # On détermine si le routeur est connecté à un peer:
    co_peer = False
    for As in dico_policies["Peer"].values():
        for lien_ebgp in dico_policies["Peer"][As]["Liens_ebgp"]:
            if routeur in lien_ebgp:
                co_peer = True

    # On détermine si le routeur est connecté à un fournisseur:
    co_fournisseur = False
    for As in dico_policies["Fournisseur"].values():
        for lien_ebgp in dico_policies["Fournisseur"][As]["Liens_ebgp"]:
            if routeur in lien_ebgp:
                co_fournisseur = True

    # Liste pour stocker les lignes modifiées
    updated_lines = []    

    # Parcourir chaque ligne, et pour chaque ligne, soit la modifier si c'est nécessaire, soit la laisser à l'identique
    for line in lines:

        if line.startswith("ip forward protocol nd"): 
            updated_lines.append("ip forward protocol nd\n!\nip bgp-community new-format\n")
            if co_client :
                updated_lines.append("ip community-list standard com_client permit 10:300\n") # On tag toutes les routes qui viennent d'un client.


        elif line.startswith("  neighbor"):
            updated_lines.append(line) # On conserve la ligne qui active le voisin bgp.
            updated_lines.append(f" neighbour 2000:100:{nb_neighbor_customer}::{nb_neighbor_customer} send community both\n") # addresse du voisin dans l'AS client
            if co_client :
                updated_lines.append(f" neighbour 2000:100:{nb_neighbor_customer}::{nb_neighbor_customer} route-map TAG_client in\n")
    

        elif line.startswith(" redistribute connected"): 
            updated_lines.append(" redistribute connected\n!\n!\n")
            if co_client:
                updated_lines.append(f"route-map TAG_client permit 10 \n set local preference 150 \n")
                updated_lines.append(f" set community 10:150 additive \n")
                updated_lines.append(f"route-map TAG_client permit 50 \n")

            elif co_peer:
                updated_lines.append(f"route-map TAG_peer permit 10 \n set local preference 100 \n")

            elif co_fournisseur:
                updated_lines.append(f"route-map TAG_provider permit 10 \n set local preference 50 \n")


        # Pour tous les routeurs de bordure
        #Cas de rip
        elif line.startswith(" redistribute connected"):
            updated_lines.append(" redistribute connected\n!\n!\n")
            updated_lines.append("route-map com_client permit 10\n")
            updated_lines.append(" match community com_client\n!\n")
            updated_lines.append("route-map com_client deny\n")
        # Cas de ospf
        elif line.startswith("ipv6 router ospf 1"):
            updated_lines.append(line)
            updated_lines.append(f" router-id {nb_router}.{nb_router}.{nb_router}.{nb_router}\n!\n!\n")
            updated_lines.append("route-map com_client permit 10\n")
            updated_lines.append(" match community com_client\n!\n")
            updated_lines.append("route-map com_client deny\n")
       
            
        else:
            updated_lines.append(line)  # Conserver les lignes inchangées


    # Écrire les modifications dans le fichier
    with open(filename, 'w') as file: # Ce fichier n'existe pas encore, il est donc créé.
        file.writelines(updated_lines)
        print(f"Ajout des policies sur le fichier de configuration de {routeur} terminées.")
