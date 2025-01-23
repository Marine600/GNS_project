# ATTENTION : ces fonctions ont été écrites pour une version optimisée du Json qui permet d'automatiser l'addressage ipv6 
# en partant seulement du préfixe de l'AS (exemple plus bas)

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

    '''
    routeurs, subnets = addressage(AS)
    interfaces = {}
    
    for router in routeurs.keys():
        addresses = routeurs[router]
        router_interface = {}
        
        router_interface["loopback 0"] = addresses[0][0:9] + f"{router[1:3]}::{router[1:3]}/64"
        router_interface["FastEthernet0/0"] = addresses[0]
        
        if len(addresses) >= 2 :
            router_interface["GigabitEthernet1/0"] = addresses[1]
            
            if len(addresses) >= 3 :
                router_interface["GigabitEthernet2/0"] = addresses[2]
                
                if len(addresses) == 4 :
                    router_interface["GigabitEthernet3/0"] = addresses[3]
                    
        interfaces[router] = router_interface

    return interfaces, subnets

# POUR TESTER
#dicoAS = {"AS" :
#               {10 :
 #                   {"Protocole" : "RIP",
  #                   "Routeurs" : ["R11", "R12", "R13", "R14", "R15", "R16", "R17"],
   #                 "Liens" : [["R11","R12"],["R11","R16"],["R11","R17"],["R12","R13"],["R12","R15"],["R12","R14"],["R13","R15"],["R14","R15"],["R15","R16"],["R16","R17"]],
    #                "Ip_range" : "2000:100:1::/54"}
     #               }}
     # pour les liens des routeurs de bordure ajouter un attribut au même niveau que l'attribut "AS" qui s'appellerait "Border" avec les routeurs de bordure et les liens
     # "Border" : {
     #              "Routers" : ["R13", "R14", "R27", "R21"],
     #              "Liens_border" : [["R13", "R21"], ["R14", "R27"]]}
    
#AS = dicoAS["AS"][10]

#plan_addressage = addressage(AS)

#print(interface(plan_addressage))


    