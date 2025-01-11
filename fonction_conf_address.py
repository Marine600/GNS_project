

def conf_address(routeur, router_id):
    # Configure les addresses IP de chaque interface d'un routeur
    # Paramètres : Dictionnaire routeur
    #              Chaine de caractères ip_range la plage d'addresse de l'AS
    #              Entier router_id
    # Retourne : Dictionnaire addresses avec comme clés les interfaces et comme valeurs les addresses IP
    #         

    addresses = {}
    voisins = []
    voisins = routeur["voisins"] # Récupérer les voisins du routeur, voisins est une liste de liste contenant les voisins et l'addresse du sous-réseau associé à la connexion

    addresses["loopback 0"] = routeur["loopback_address"] # On configure l'addresse loopback
    
    addresses["FastEthernet0/0"] = voisins[0][1] + f"{router_id}/64"
    if len(voisins) >= 2 :
        addresses["GigabitEthernet1/0"] = voisins[1][1] + f"{router_id}/64"

        if len(voisins) >= 3 :
            addresses["GigabitEthernet2/0"] = voisins[2][1] + f"{router_id}/64"

            if len(voisins) == 4 :
                addresses["GigabitEthernet3/0"] = voisins[3][1] + f"{routeur_id}/64"

    return addresses

    