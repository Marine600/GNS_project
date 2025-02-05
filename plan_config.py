import fonction_conf_address
import json

with open("GNS.json", 'r') as json_file:
    intent = json.load(json_file)

interfaces_dispos = {"FastEthernet0/0", "GigabitEthernet1/0", "GigabitEthernet2/0", "GigabitEthernet3/0"}

def plan_config(dicoAS):
    liens_AS = dicoAS["Liens"]
    interfaces, subnets = fonction_conf_address.interface(dicoAS)
    plan = {}

    # Initialisation du dictionnaire resultat plan avec les clés qui sont les routeurs de l'AS 
    for router in dicoAS["Routeurs"]:
        plan[router] = {}
    
    # Creation du dictionnaire qu'on mettra à jour au fur et à mesure avec les interfaces utilisées de chaque routeur
    used_interfaces = {}
    for router in dicoAS["Routeurs"]:
        used_interfaces[router] = set()
    
    # On parcourt la liste des liens de l'AS
    for lien in liens_AS:
        router1 = lien[0] # On récupère le premier routeur du lien
        router2 = lien[1] # On récupère le deuxième routeur du lien
        addresses_R1 = interfaces.get(router1, {}) # On récupère les dictionnaires correspondant aux routeurs et contenant la config de chaque interface
        addresses_R2 = interfaces.get(router2, {})
        
        for inter1, add1 in addresses_R1.items():
            if inter1 not in interfaces_dispos or inter1 in used_interfaces[router1]:
                continue
            
            for inter2, add2 in addresses_R2.items():
                if inter2 not in interfaces_dispos or inter2 in used_interfaces[router2]:
                    continue
                
                # Ensure addresses are in the same subnet
                if dicoAS["Protocol"] == "OSPF":
                    if add1[0][:12] == add2[0][:12]:
                        plan[router1][inter1] = router2
                        plan[router2][inter2] = router1
                        used_interfaces[router1].add(inter1)
                        used_interfaces[router2].add(inter2)
                        break  # Stop after finding a valid pair
                else:
                    if add1[:12] == add2[:12]:
                        plan[router1][inter1] = router2
                        plan[router2][inter2] = router1
                        used_interfaces[router1].add(inter1)
                        used_interfaces[router2].add(inter2)
                        break  # Stop after finding a valid pair
    
    return plan

if __name__ == "__main__":
    for AS_number in intent["AS"].keys():
        print(f"############## CONFIG POUR L'AS{AS_number} ##############")
        print(plan_config(intent["AS"][AS_number]))
        print("\n")

