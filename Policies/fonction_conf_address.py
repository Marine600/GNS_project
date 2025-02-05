# Interfaces disponibles sur les routeurs 
interfaces_dispos = ["FastEthernet0/0", "GigabitEthernet1/0", "GigabitEthernet2/0", "GigabitEthernet3/0"]

def addressage(AS):
    '''
    Prend en paramètre un AS et attribut à chaque routeur des addresses ipv6 adaptées

    Parameters
    ----------
    AS : Dictionnaire 
        Contient les propriétés de l'AS dont une clé Liens qui est une liste de listes des liens entre les routeurs

    Returns
    -------
    dic : Dictionnaire
        Dictionnaire des addresses ipv6 configurées pour chaque routeur :
        clé = routeur
        valeur = liste de listes [["adresse ip", "cout du lien ospf"]] si OSPF
        valeur = liste des adresses ip si RIP
    subnet : Liste des subnets de l'AS

    '''
    dic = {}
    subnet = []
    
    # On parcourt les liens de l'AS
    for i in range(len(AS["Liens"])):
        
        # On rajoute chaque routeur dans le dictionnaire dic
        if AS["Liens"][i][0] not in dic.keys():

            # On configure l'addresse ipv6 du routeur à partir du l'ip range de l'AS
            adresse = AS["Ip_range"][0:11] + f"{i+1}::" + AS["Liens"][i][0][1:3] + "/64"

            # Si OSPF est configuré dans l'AS on rajoute la métrique
            if AS["Protocol"] == "OSPF":
                dic[AS["Liens"][i][0]] = [[adresse,AS["Liens"][i][2]]]

            else :
                dic[AS["Liens"][i][0]] = [adresse]

        else:
            adresse = AS["Ip_range"][0:11] + f"{i+1}::" + AS["Liens"][i][0][1:3] + "/64"

            if AS["Protocol"] == "OSPF":
                dic[AS["Liens"][i][0]].append([adresse, AS["Liens"][i][2]])

            else :
                dic[AS["Liens"][i][0]].append(adresse) 
            
            
        if AS["Liens"][i][1] not in dic.keys():
            adresse = AS["Ip_range"][0:11] + f"{i+1}::" + AS["Liens"][i][1][1:3] + "/64"

            if AS["Protocol"] == "OSPF":
                dic[AS["Liens"][i][1]] = [[adresse,AS["Liens"][i][2]]]

            else :
                dic[AS["Liens"][i][1]] = [adresse]

        else:
            adresse = AS["Ip_range"][0:11] + f"{i+1}::" + AS["Liens"][i][1][1:3] + "/64"

            if AS["Protocol"] == "OSPF":
                    dic[AS["Liens"][i][1]].append([adresse, AS["Liens"][i][2]])
            
            else :
                dic[AS["Liens"][i][1]].append(adresse)
        
        subnet.append(AS["Ip_range"][0:11] + f"{i+1}::" + "/64")
        
    return dic, subnet

def interface(AS):
    '''
    

    Parameters
    ----------
    routeurs : Dictionnaire renvoyé par la fonction addressage

    Returns
    -------
    interfaces : Dictionnaire avec comme clés les routeurs et comme valeurs un dictionnaire des noms des interfaces configurées et de leurs addresses ip respectives
    clé = routeur
    valeur = dictionnaire avec comme clé les interfaces configurées et comme valeur l'adresse ip correspondante (si RIP) ou une liste contenant l'adresse ip correspondante et le cout du lien OSPF
    subnets : Liste des subnets de l'AS
    '''
    routeurs, subnets = addressage(AS)
    interfaces = {}
    
    for router in routeurs.keys():
        addresses = routeurs[router]
        router_interface = {}
        
        if AS["Protocol"] == "OSPF" :
            router_interface["Loopback0"] = [(addresses[0][0])[0:9] + f"{router[1:3]}::{router[1:3]}/128", addresses[0][1]]
            router_interface[interfaces_dispos[0]] = [addresses[0][0],addresses[0][1]]
            
            if len(addresses) >= 2 :
                router_interface[interfaces_dispos[1]] = [addresses[1][0],addresses[1][1]]
                
                if len(addresses) >= 3 :
                    router_interface[interfaces_dispos[2]] = [addresses[2][0],addresses[2][1]]
                    
                    if len(addresses) == 4 :
                        router_interface[interfaces_dispos[3]] = [addresses[3][0],addresses[3][1]]

        else :
            router_interface["Loopback0"] = addresses[0][0:9] + f"{router[1:3]}::{router[1:3]}/128"
            router_interface[interfaces_dispos[0]] = addresses[0]
            
            if len(addresses) >= 2 :
                router_interface[interfaces_dispos[1]] = addresses[1]
                
                if len(addresses) >= 3 :
                    router_interface[interfaces_dispos[2]] = addresses[2]
                    
                    if len(addresses) == 4 :
                        router_interface[interfaces_dispos[3]] = addresses[3]
                    
        interfaces[router] = router_interface

    return interfaces, subnets

def border(border_dico):
    '''
    Parameters
    ----------
    border_dico : Dictionnaire decrivant les liens inter-AS

    Returns
    -------
    inter : Dictionnaire avec comme clés les routeurs et comme valeurs un dictionnaire des noms des interfaces configurées et de leurs addresses ip respectives
    '''
    dic_temp = {}
    inter = {}
    for i in range(len(border_dico["Liens_border"])):
        
        if border_dico["Liens_border"][i][0] not in dic_temp.keys():
            dic_temp[border_dico["Liens_border"][i][0]] = [border_dico["Ip_range"][0:11] + f"{i+1}::" + border_dico["Liens_border"][i][0][1:3] + "/64"]
        else:
            dic_temp[border_dico["Liens_border"]].append(border_dico["Ip_range"][0:11] + f"{i+1}::" + border_dico["Liens_border"][i][0][1:3] + "/64")
            
        if border_dico["Liens_border"][i][1] not in dic_temp.keys():
            dic_temp[border_dico["Liens_border"][i][1]] = [border_dico["Ip_range"][0:11] + f"{i+1}::" + border_dico["Liens_border"][i][1][1:3] + "/64"]
        else:
            dic_temp[border_dico["Liens_border"][i][1]].append(border_dico["Ip_range"][0:11] + f"{i+1}::" + border_dico["Liens_border"][i][1][1:3] + "/64")

    for router in dic_temp.keys():
        addresses = dic_temp[router]
        router_interface = {}

        router_interface[interfaces_dispos[3]] = addresses[0]
                    
        inter[router] = router_interface
    
    return inter
