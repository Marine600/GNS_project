import json
import fonction_conf_address

def modif_config(filename, lines, dico, dicoAS, routeur):

    # id du routeur
    number = routeur[1] + routeur[2] #Prendre uniquement le numero du routeur
    routeur_id = number+"."+number+"."+number+"."+number

    # Détermination du nom de l'AS
    if routeur[1] == "1":
        as_name = "10"
    else:
        as_name = "20"

    protocol = dico["AS"][as_name]["Protocol"]

    dico_interfaces, liste_subnet = fonction_conf_address.interface(dicoAS)
    dico_interfaces_routeur = dico_interfaces[routeur]
    dico_border = fonction_conf_address.border(dico["Border"])

    # Liste pour stocker les lignes modifiées
    updated_lines = []

    # Récupérer l'info sur si le routeur est en ebgp ou pas, à partir des données JSON
    ebgp = False
    if routeur in dico["Border"]["Routers"]:
        ebgp = True

    # Parcourir chaque ligne, et pour chaque ligne, soit la modifier si c'est nécessaire, soit la laisser à l'identique
    for line in lines:


        if line.startswith("hostname"):  # Modifier le hostname
            updated_lines.append(f"hostname {routeur}\n")


        # Modifier l'interface Loopback
        # ATTENTION: sur certaines lignes, comme par exemple sur la suivante, il y a un espace avant le texte dans le fichier json : NE PAS L'OUBLIER !
        elif line.startswith(" ipv6 address 4000"): # On a rajouté le 4000 car il y a plusieurs lignes dans le json qui commencent par ipv6 address.
            updated_lines.append(f" ipv6 address {dico_interfaces_routeur['Loopback0']}\n")


        elif line.startswith("interface FastEthernet0/0"): # Tous les routeurs ont une interface FastEthernet0/0
            updated_lines.append("interface FastEthernet0/0\n")
            updated_lines.append(" no ip address\n")

            if ebgp: # Routeurs de bordure
                updated_lines.append(" duplex full\n") # duplex full que pour fastethernet
                updated_lines.append(f" ipv6 address {dico_interfaces_routeur['FastEthernet0/0']}\n") #Ajout address
                updated_lines.append(" ipv6 enable\n")# même chose pour bordure ou non : peut être à modifier
                if protocol == "RIP": # même chose pour bordure ou non : peut être à modifier
                    updated_lines.append(" ipv6 rip ng enable\n")# même chose pour bordure ou non : peut être à modifier
                if protocol == "OSPF":# même chose pour bordure ou non : peut être à modifier
                    updated_lines.append(" ipv6 ospf 1 area 0\n")# même chose pour bordure ou non : peut être à modifier
            
            else:
                updated_lines.append(" negotiation auto\n")
                updated_lines.append(f" ipv6 address {dico_interfaces_routeur['FastEthernet0/0']}\n") #Ajout address
                updated_lines.append(" ipv6 enable\n")# même chose pour bordure ou non : peut être à modifier
                if protocol == "RIP":# même chose pour bordure ou non : peut être à modifier
                    updated_lines.append(" ipv6 rip ng enable\n")# même chose pour bordure ou non : peut être à modifier
                if protocol == "OSPF":# même chose pour bordure ou non : peut être à modifier
                    updated_lines.append(" ipv6 ospf 1 area 0\n")# même chose pour bordure ou non : peut être à modifier

# Faire une fonction pour éviter la répétition entre chaque interface
        elif line.startswith("interface GigabitEthernet1/0"): # Tous les routeurs ont une interface GigabitEthernet1/0
            updated_lines.append("interface GigabitEthernet1/0\n")
            updated_lines.append(" no ip address\n")

            if ebgp: # Routeurs de bordure
                updated_lines.append(f" ipv6 address {dico_interfaces_routeur['GigabitEthernet1/0']}\n") #Ajout address
                updated_lines.append(" ipv6 enable\n")# même chose pour bordure ou non : peut être à modifier
                if protocol == "RIP": # même chose pour bordure ou non : peut être à modifier
                    updated_lines.append(" ipv6 rip ng enable\n")# même chose pour bordure ou non : peut être à modifier
                if protocol == "OSPF":# même chose pour bordure ou non : peut être à modifier
                    updated_lines.append(" ipv6 ospf 1 area 0\n")# même chose pour bordure ou non : peut être à modifier
            
            else:
                updated_lines.append(" negotiation auto\n")
                updated_lines.append(f" ipv6 address {dico_interfaces_routeur['GigabitEthernet1/0']}\n") #Ajout address
                updated_lines.append(" ipv6 enable\n")# même chose pour bordure ou non : peut être à modifier
                if protocol == "RIP":# même chose pour bordure ou non : peut être à modifier
                    updated_lines.append(" ipv6 rip ng enable\n")# même chose pour bordure ou non : peut être à modifier
                if protocol == "OSPF":# même chose pour bordure ou non : peut être à modifier
                    updated_lines.append(" ipv6 ospf 1 area 0\n")# même chose pour bordure ou non : peut être à modifier


        elif line.startswith("interface GigabitEthernet2/0"): # Tous les routeurs n'ont pas une interface GigabitEthernet2/0
            updated_lines.append("interface GigabitEthernet2/0\n")
            updated_lines.append(" no ip address\n")
            if "GigabitEthernet2/0" in dico_interfaces_routeur.keys():
                
                if ebgp: # Routeurs de bordure
                    updated_lines.append(f" ipv6 address {dico_interfaces_routeur['GigabitEthernet2/0']}\n") #Ajout address
                    updated_lines.append(" ipv6 enable\n")# même chose pour bordure ou non : peut être à modifier
                    if protocol == "RIP": # même chose pour bordure ou non : peut être à modifier
                        updated_lines.append(" ipv6 rip ng enable\n")# même chose pour bordure ou non : peut être à modifier
                    if protocol == "OSPF":# même chose pour bordure ou non : peut être à modifier
                        updated_lines.append(" ipv6 ospf 1 area 0\n")# même chose pour bordure ou non : peut être à modifier
                
                else:
                    updated_lines.append(" negotiation auto\n")
                    updated_lines.append(f" ipv6 address {dico_interfaces_routeur['GigabitEthernet2/0']}\n") #Ajout address
                    updated_lines.append(" ipv6 enable\n")# même chose pour bordure ou non : peut être à modifier
                    if protocol == "RIP":# même chose pour bordure ou non : peut être à modifier
                        updated_lines.append(" ipv6 rip ng enable\n")# même chose pour bordure ou non : peut être à modifier
                    if protocol == "OSPF":# même chose pour bordure ou non : peut être à modifier
                        updated_lines.append(" ipv6 ospf 1 area 0\n")# même chose pour bordure ou non : peut être à modifier
            else:
                updated_lines.append(" shutdown\n")
                updated_lines.append(" negotiation auto\n")

        
        elif line.startswith("interface GigabitEthernet3/0"): # Tous les routeurs n'ont pas une interface GigabitEthernet3/0
            updated_lines.append("interface GigabitEthernet3/0\n")
            updated_lines.append(" no ip address\n")
            if "GigabitEthernet3/0" in dico_interfaces_routeur.keys(): #On entre dans cette boucle si le routeur est en ibgp et qu'il a une interface GigabitEthernet3/0
                
                updated_lines.append(" negotiation auto\n")
                updated_lines.append(f" ipv6 address {dico_interfaces_routeur['GigabitEthernet3/0']}\n") #Ajout address
                updated_lines.append(" ipv6 enable\n")# même chose pour bordure ou non : peut être à modifier
                if protocol == "RIP":# même chose pour bordure ou non : peut être à modifier
                    updated_lines.append(" ipv6 rip ng enable\n")# même chose pour bordure ou non : peut être à modifier
                if protocol == "OSPF":# même chose pour bordure ou non : peut être à modifier
                    updated_lines.append(" ipv6 ospf 1 area 0\n")# même chose pour bordure ou non : peut être à modifier
            
            elif ebgp: # Tous les routeurs en ebgp ont une interface GigabitEthernet3/0, c'est celle qui fait le lien entre 2 AS.
                updated_lines.append(f" ipv6 address {dico_border[routeur]['GigabitEthernet3/0']}\n") #Les liens entre 2 AS ne sont pas présent dans dico_interfaces_routeur mais dans dico_border.
                updated_lines.append(" ipv6 enable\n")# même chose pour bordure ou non : peut être à modifier
                if protocol == "RIP": # même chose pour bordure ou non : peut être à modifier
                    updated_lines.append(" ipv6 rip ng enable\n")# même chose pour bordure ou non : peut être à modifier
                if protocol == "OSPF":# même chose pour bordure ou non : peut être à modifier
                    updated_lines.append(" ipv6 ospf 1 area 0\n")# même chose pour bordure ou non : peut être à modifier
            else:
                updated_lines.append(" shutdown\n")
                updated_lines.append(" negotiation auto\n")
            

        elif line.startswith("router bgp"):  # Modifier le router bgp
            updated_lines.append(f" router bgp {as_name}\n")


        elif line.startswith(" bgp router-id"):  # Modifier le router-id
            updated_lines.append(f" bgp router-id {routeur_id}\n")


        elif line.startswith(" no bgp default ipv4-unicast"):
            updated_lines.append(" no bgp default ipv4-unicast\n")
            for voisin_bgp in dico["AS"][as_name]["Routeurs"]: # On parcourt tous les routeurs de l'AS
                if voisin_bgp != routeur: # Attention un routeur n'est pas voisin de lui même
                    loop_voisin = dico_interfaces[voisin_bgp]['Loopback0']
                    updated_lines.append(f" neighbor {loop_voisin[0:-4]} remote-as {as_name}\n")
                    updated_lines.append(f" neighbor {loop_voisin[0:-4]} update-source Loopback0\n")
            if ebgp:
                if as_name == "20":
                    autre_as = "10"
                else:
                    autre_as = "20"
                for lien in dico["Border"]["Liens_border"]: # On cherche le voisin ebgp de notre routeur
                    if lien[0] == routeur:
                        voisin_ebgp = lien[1]
                    if lien[1]==routeur:
                        voisin_ebgp = lien[0]
                ad_voisin_ebgp = dico_border[voisin_ebgp]["GigabitEthernet3/0"]
                updated_lines.append(f" neighbor {ad_voisin_ebgp[0:-3]} remote-as {autre_as}\n") # Voisin d'une autre AS


        elif line.startswith(" address-family ipv6"): #  Les routeurs de bordure advertise tous les sous-réseaux internes à l'AS.
            updated_lines.append(" address-family ipv6\n")
            if ebgp:
                for subnet in liste_subnet:
                    updated_lines.append(f"  network {subnet}\n")
                updated_lines.append(f"  neighbor {ad_voisin_ebgp[0:-3]} activate\n")
            
            for voisin_bgp in dico["AS"][as_name]["Routeurs"]: # On active tous les voisins
                if voisin_bgp != routeur: # Attention un routeur n'est pas voisin de lui même
                    loop_voisin = dico_interfaces[voisin_bgp]['Loopback0']
                    updated_lines.append(f"  neighbor {loop_voisin[0:-4]} activate\n")


        elif line.startswith("ipv6 router ospf 1"):
            updated_lines.append(f"ipv6 router ospf 1\n router-id {routeur_id}\n ")
            if ebgp:
                updated_lines.append("passive-interface GigabitEthernet3/0\n ")  
        
        
        else:
            updated_lines.append(line)  # Conserver les lignes inchangées


    # Écrire les modifications dans le fichier
    with open(filename, 'w') as file: # Ce fichier n'existe pas encore, il est donc créé
        file.writelines(updated_lines)
        print(f"Modifications du fichier de configuration de {routeur} terminées.")






if __name__=="__main__":
    # Charger le fichier JSON
    with open ("GNS.json", 'r') as json_file:
        dico = json.load(json_file)

    # Parcourir chaque AS dans le fichier JSON
    for dicoAS in dico["AS"].values():
        # Lire le fichier modèle rip ou ospf en fonction de l'AS dans lequel se trouve le routeur
        if dicoAS["Protocol"] == "RIP":
            with open("model_RIP_startup-config.cfg", 'r') as file:
                lines = file.readlines()  # Lire toutes les lignes du fichier
        else:
            with open("model_OSPF_startup-config.cfg", 'r') as file:
                lines = file.readlines() # lines = contenu du fichier modèle

        # Parcourir chaque routeur de l'AS
        for routeur in dicoAS["Routeurs"]:
            # Nom du fichier de configuration créé basé sur le nom du routeur
            filename = f"i{routeur[1]+routeur[2]}_startup-config.cfg"
            modif_config(filename, lines, dico, dicoAS, routeur) #Modifie le fichier modèle d'un routeur
    
 # type: ignore
