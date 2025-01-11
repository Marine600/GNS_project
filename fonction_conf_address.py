

def conf_address(routeur, ip_range, router_id, liens, numero_AS):
    # Configure les addresses IP de chaque interface d'un routeur
    # Paramètres : Dictionnaire routeur
    #              Chaine de caractères ip_range la plage d'addresse de l'AS
    #              Entier router_id
    #              Entier numero_AS
    #              Dictionnaire liens avec comme clés les 2 routeurs d'une connexion et comme valeurs l'addresse IP du sous-réseau
    # Retourne : Dictionnaire addresses avec comme clés les interfaces et comme valeurs les addresses IP
    #            Dictionnaire liens 

    addresses = {}
    voisins = []
    voisins = routeur["voisins"] # Récupérer les voisins du routeur

    addresses["loopback 0"] = routeur["loopback_address"] # On configure l'addresse loopback

    # Traitement des routeurs de bordure
    if routeur["eBGP"] == True : # On regarde si on a un routeur de bordure
        if numero_AS == 20



    if (f"router_id - {voisins[0]}" in liens.keys()) or (f"{voisins[0]} - router_id" in liens.keys()): # On regarde si on a déjà attribué au lien routeur-voisin une addresse ip

        addresses["FastEthernet0/0"] = liens[f"router_id - {voisins[0]}"] + f"{router_id}/64"

        if (len(voisins) == 2) and (f"router_id - {voisins[1]}" in liens.keys()) or (f"{voisins[1]} - router_id" in liens.keys()) :
            addresses["GigabitEthernet1/0"] = liens[f"router_id - {voisins[1]}"] + f"{router_id}/64"

            if (len(voisins) == 3) and (f"router_id - {voisins[2]}" in liens.keys()) or (f"{voisins[2]} - router_id" in liens.keys()) :
                addresses["GigabitEthernet2/0"] = liens[f"router_id - {voisins[2]}"] + f"{router_id}/64"

                if (len(voisins) == 4) and (f"router_id - {voisins[3]}" in liens.keys()) or (f"{voisins[3]} - router_id" in liens.keys()) :
                    addresses["GigabitEthernet3/0"] = liens[f"router_id - {voisins[3]}"] + f"{router_id}/64"
     


     
    
    liens[f"{routeur.keys()}-{voisins[0]}"] = "ip_range" + f"{numero_lien}::" 

    return addresses, liens

    