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
        Dictionnaire des addresses ipv6 configurées pour chaque routeur
    subnet : Liste des subnets de l'AS

    '''
    dic = {}
    subnet = []
    
    for i in range(len(AS["Liens"])):
        
        if AS["Liens"][i][0] not in dic.keys():
            dic[AS["Liens"][i][0]] = [AS["Ip_range"][0:11] + f"{i+1}::" + AS["Liens"][i][0][1:3] + "/64"]
        else:
            dic[AS["Liens"][i][0]].append(AS["Ip_range"][0:11] + f"{i+1}::" + AS["Liens"][i][0][1:3] + "/64")
            
        if AS["Liens"][i][1] not in dic.keys():
            dic[AS["Liens"][i][1]] = [AS["Ip_range"][0:11] + f"{i+1}::" + AS["Liens"][i][1][1:3] + "/64"]
        else:
            dic[AS["Liens"][i][1]].append(AS["Ip_range"][0:11] + f"{i+1}::" + AS["Liens"][i][1][1:3] + "/64")
        
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
    subnets : Liste des subnets de l'AS
    '''
    routeurs, subnets = addressage(AS)
    interfaces = {}
    
    for router in routeurs.keys():
        addresses = routeurs[router]
        router_interface = {}
        
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




    