import json
import fonction_conf_address

def modif_config(lines, router_data, router_name, as_name, protocol):
        
    address_routeur = fonction_conf_address.conf_address(router_name)

    # Liste pour stocker les lignes modifiées
    updated_lines = []

    # Récupérer l'info sur si le routeur est en ebgp ou pas, à partir des données JSON
    number = router_name[1] + router_name[2] #Prendre uniquement le numero du routeur
    routeur_id = number+"."+number+"."+number+"."+number
    ebgp = router_data.get("eBGP", False)

    # Parcourir chaque ligne, et pour chaque ligne, soit la modifier si c'est nécessaire, soit la laisser à l'identique
    for line in lines:

        if line.startswith("hostname"):  # Modifier le hostname
            updated_lines.append("hostname {router_name}\n")

        elif line.startswith("interface Loopback"):  # Modifier l'interface Loopback'
            updated_lines.append("interface Loopback{router_name}\n")

        elif line.startswith("ipv6 address 4000"):  # Modifier l'interface Loopback'
            updated_lines.append("ipv6 address {routeur_data.get('loopback_address')}\n")  #A modifier pb il y a plein de lignes qui commencent avec ipv6 address

        elif line.startswith("FastEthernet0/0"):  # A modifier, on a toujours cette interface
            updated_lines.append("FastEthernet0/0")
            if "FastEthernet0/0" not in address_routeur.key():
                updated_lines.append("no ip address\n shutdown\n negotiation auto\n")
            else:
                updated_lines.append("no ip address\n")
                if ebgp:
                    updated_lines.append("duplex full\n")
                    updated_lines.append("ipv6 address\n") #Ajout address
                    updated_lines.append("ipv6 enable\n")
                    if protocol == "rip":
                        updated_lines.append("ipv6 rip ng enable\n") #Cas particulier à modifier
                    if protocol == "ospf": #Cas part
                        updated_lines.append("ipv6 ospf 1 area 0\n") #Cas particulier à modifier
                else:
                    updated_lines.append("negotiation auto\n")
                    updated_lines.append("ipv6 address {address_routeur['FastEthernet0/0']}\n") #Ajout address
                    updated_lines.append("ipv6 enable\n")
                    if as_name=="10": #On utilise le protocol RIP
                        updated_lines.append("ipv6 rip ng enable\n")
                    if as_name=="20": #On utilise ospf
                        updated_lines.append("ipv6 ospf 1 area 0\n")
            
        elif line.startswith("router bgp"):  # Modifier le router bgp
            updated_lines.append("router bgp {as_name}\n")

        elif line.startswith("bgp router-id"):  # Modifier le router-id
            updated_lines.append("bgp router-id {router_id}\n")

        elif line.startswith("no bgp default ipv4-unicast"):  # Modifier le router-id
            updated_lines.append("no bgp default ipv4-unicast\n")
            if ibgp:  #Modif Yassmine
                for voisin in router_data.get("voisins"):
                    nom_voisin = router_name.get("voisin"[0])
                    number_voisin = nom_voisin[1] + nom_voisin[2]
                    add_loop_voisin = "2000:100:"+number_voisin+"::"+number_voisin
                    updated_lines.append("neighbor {add_loop_voisin} remote-as {as_name}\n")
                    updated_lines.append("neighbor {add_loop_voisin} update-source Loopback{number}\n")
            else:
                for voisin in router_data.get("voisins"):
                    nom_voisin = router_name.get("voisin"[0])
                    number_voisin = nom_voisin[1] + nom_voisin[2]
                    add_loop_voisin = "2000:100:"+number_voisin+"::"+number_voisin
                    updated_lines.append("neighbor {add_loop_voisin} remote-as {as_name}\n") #Modifier as_name
        
        elif line.startswith("address-family ipv6"):
            updated_lines.append("address-family ipv6\n")
            for voisin in router_data.get("voisins"):
                nom_voisin = router_name.get("voisin"[0])
                number_voisin = nom_voisin[1] + nom_voisin[2]
                add_loop_voisin = "2000:100:"+number_voisin+"::"+number_voisin
                updated_lines.append("neighbor {add_loop_voisin} activate\n")

        elif line.startswith("ipv6 router"):
            if ebgp:
                if protocol=="rip":
                    updated_lines.append("ipv6 router rip ng\n  reditribute connected\n ") #### A modifier
                if protocol=="ospf":
                    updated_lines.append("ipv6 router ospf 1\n router-id\n  passive-interface FastEthernet0/0\n ")  
            else:
                if protocol=="rip":
                    updated_lines.append("ipv6 router rip ng\n  reditribute connected\n ")
                if protocol=="ospf":
                    updated_lines.append("ipv6 router ospf 1\n ")
        
        else:
            updated_lines.append(line)  # Conserver les lignes inchangées

    # Écrire les modifications dans le fichier
    with open('model_RIP_startup-config.cfg', 'w') as file:
        file.writelines(updated_lines)


if __name__=="__main__":
    # Charger le fichier JSON
    with open ("model_RIP_startup-config.cfg", 'r') as json_file:
        data = json.load(json_file)

    # Parcourir chaque AS dans le fichier JSON
    for as_name, as_data in data.items():
        protocol = as_data.get("protocol", "unknown")  # Récupérer le protocole utilisé par l'AS
        routeurs = as_data.get("routeurs", {}) #Récupérer les routeurs présents dans chaque AS

        # Parcourir chaque routeur dans l'AS
        for router_name, router_data in routeurs.items():
            # Nom du fichier basé sur le nom du routeur
            filename = f"i{router_name[1]+router_name[2]}_startup-config.cfg"

            # Lire le fichier existant et remplacer certaines informations
            if as_name == "10":
                protocol="rip"
                with open('model_rip_config.cfg', 'r') as file:
                    lines = file.readlines()  # Lire toutes les lignes du fichier
            else:
                protocol="ospf"
                with open('model_ospf_config.cfg', 'r') as file:
                    lines = file.readlines()  # Lire toutes les lignes du fichier

            modif_config(lines,router_data,router_name,as_name,protocol)

            print("Modifications du fichier de configuration de {routeur_name} terminées.")
    
 # type: ignore
