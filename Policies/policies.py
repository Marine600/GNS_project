import json


# On applique cette fonction à tous les routeurs de bordure de notre AS après leur avoir préalablement appliqué la fonction de configuration de base.
def modif_config_policies(lines, dico_policies, routeur, filename):
    
    # Liste pour stocker les lignes modifiées
    updated_lines = []    


    # Parcourir chaque ligne, et pour chaque ligne, soit la modifier si c'est nécessaire, soit la laisser à l'identique
    for line in lines:


        if line.startswith("ip forward protocol nd"): 
            updated_lines.append("ip forward protocol nd\n!\nip bgp-community new-format\n")
            if #routeur de bordure connecté à une AS client :
                updated_lines.append("ip community-list standard com_client permit 10:300\n") # On tag toutes les routes qui viennent d'un client.


        elif line.startswith("  neighbor"):
            updated_lines.append(line) # On conserve la ligne qui active le voisin bgp.
            updated_lines.append(f" neighbour {adresse_voisin AS client} send community both\n")
            if #routeur de bordure connecté à une AS client :
                updated_lines.append(f" neighbour {adresse_voisin AS client} route-map {TAG_AS_NUMBER} in\n")
    

        elif line.startswith(" redistribute connected"): 
            updated_lines.append(" redistribute connected\n!\n!\n")
            if # routeur connecté à un client:
                updated_lines.append(f"route-map {TAG_AS_NUMBER} permit 10 \n set local preference 150 \n")
                updated_lines.append(f" set community 10:150 additive \n")
                updated_lines.append(f"route-map {TAG_AS_NUMBER} permit 50 \n")


            elif # routeur connecté à un peer:
            updated_lines.append(f"route-map {TAG_AS_NUMBER} permit 10 \n set local preference 100 \n")


            elif # routeur connecté à un fournisseur:
            updated_lines.append(f"route-map {TAG_AS_NUMBER} permit 10 \n set local preference 50 \n")


        # ajouter dans le fichier modèle un indicateur pour pouvoir détecter quand ajouter les lignes suivantes
        # Pour tous les routeurs de bordure
        elif line.startswith("ipv6 router rip enable ou équivalent ospf"):
            updated_lines.append("ipv6 router rip enable ou équivalent ospf\n!\n")

            updated_lines.append("route-map com_client permit 10\n")
            updated_lines.append(" match community com_client\n!\n")
            updated_lines.append("route-map com_client deny\n")
       
            
        else:
            updated_lines.append(line)  # Conserver les lignes inchangées


    # Écrire les modifications dans le fichier
    with open(filename, 'w') as file: # Ce fichier n'existe pas encore, il est donc créé
        file.writelines(updated_lines)
        print(f"Ajout des policies sur le fichier de configuration de {routeur} terminées.")
