

def conf_address(routeur, ip_range):
    # Configure les addresses IP de chaque interface d'un routeur
    # Paramètres : Dictionnaire routeur, str ip_range la plage d'addresse de l'AS
    # Retourne : Dictionnaire addresses avec comme clés les interfaces et comme valeurs les addresses IP
    #            Dictionnaire liens avec comme clés les 2 routeurs d'une connexion et comme valeurs l'addresse IP du sous-réseau

    addresses = {}
    liens = {}
    voisins = []
    
    # Récupérer les voisins du routeur
    voisins = routeur.get("voisins", "")

     
    

    return addresses, liens

    