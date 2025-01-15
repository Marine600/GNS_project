
#ATTENTION : ne pas oublier de modifier attribut voisins en liste de listes pour que ça marche 
# on aura un truc pour R11 qui ressemble à "voisins": [["R12","2000:100:1:1::/64"],["R16","2000:100:1:2::/64"],["R17","2000:100:1:3::/64"]]

def conf_address(routeur):
    # Configure les addresses IP de chaque interface d'un routeur
    # Paramètres : Dictionnaire routeur
    # Retourne : Dictionnaire addresses avec comme clés les interfaces et comme valeurs les addresses IP
    #         

    addresses = {}
    voisins = []
    R_id = routeur["router_id"] # Récupérer l'id du routeur
    voisins = routeur["voisins"] # Récupérer les voisins du routeur, voisins est une liste de liste contenant les voisins et l'addresse du sous-réseau associé à la connexion

    addresses["loopback 0"] = routeur["loopback_address"] # On configure l'addresse loopback
    
    addresses["FastEthernet0/0"] = voisins[0][1][0:14] + f"{R_id[0:2]}/64"
    if len(voisins) >= 2 :
        addresses["GigabitEthernet1/0"] = voisins[1][1][0:14] + f"{R_id[0:2]}/64"

        if len(voisins) >= 3 :
            addresses["GigabitEthernet2/0"] = voisins[2][1][0:14] + f"{R_id[0:2]}/64"

            if len(voisins) == 4 :
                addresses["GigabitEthernet3/0"] = voisins[3][1][0:14] + f"{R_id[0:2]}/64"

    # Ajouter l'addresse du network à advertise sur une des interfaces
    if routeur["network"] != null :
        addresses["GigabitEthernet3/0"] = routeur["network"][0:14] + "1/64"


    return addresses

    