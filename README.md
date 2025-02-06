# Description du projet GNS
Projet visant à automatiser un réseau constitué de plusieurs routeurs organisés en différents AS.  
L'architecture du réseau est décrite dans le fichier _GNS.json_, qui peut être adapté. Il est important de noter que le programme n'est adapté que pour des AS configurés soit en RIP soit en OSPF, pour ce qui est de l'IGP, et en BGP.  
  
Le fichier .json contient entre autres : le nom de l'AS, ses routeurs, les liens/connections physiques entre les routeurs au sein de l'AS, le protocol de routage utilisé, la plage d'adresses ipv6 de l'AS et les liens économiques existant entre les voisins et l'AS considéré. Les liens inter-AS sont décrits dans la clé "Border".  
Dans le cas d'un routage interne réalisé grâce à OSPF, il est possible de modifier le coût des liens : il suffit d'adapter la valeur de la bande de référence dans la clé "Bandwidth" et d'adapter le coût du lien considéré en modifiant le troisième élément de chaque liste contenue dans "Liens".  
  
Dans le cadre de notre projet et pour faciliter la démonstration réalisée en classe, nous avons créé un dossier nommé _Policies_ contenant une fonction supplémentaire permettant de régler le routage BGP en respectant les relations existant entre les AS. 

# Structure du projet
- **Fichier d'intention GNS.json**  
    - Description de chaque AS : routeurs, protocol de routage interne, coûts OSPF, liens entre routeurs de l'AS, relations avec les AS voisins, plage d'adresses ipv6
    - Description de l'environnement inter-AS : routeurs, liens entre routeurs, plage d'adresses ipv6
- **fonction_conf_address.py**
    - Fonction _adressage_ qui permet d'attribuer à chaque routeur des adresses ip en fonction des liens existant au sein de l'AS et à partir de la plage d'adresses ip
    - Fonction _interface_ qui attribue, pour chaque routeur, une interface à chacune de ses adresses ip
    - Fonction _border_ qui effectue le même travail mais pour les interfaces de bordure de chaque routeur de bordure
- **policies.py**
    - Modifie le fichier de configuration d'un routeur de bordure pour prendre en compte les policies : configure les local-preference des routes en inbound, tag les routes des clients avec des communautés, crée des route-map qui filtrent en outbound tout sauf les routes tagguées
    - Possibilité de modifier les valeurs des local-pref et des communautés dans les constantes _loc_pref_ et _comm_values_
- **drag_and_drop.py**
    - Bot qui place les fichiers de configuration générés dans les dossiers correspondant aux routeurs
    - Chemin à adapter s'il le faut dans le script
- **main.py**
    - Fonction _modif_config_ qui génère le fichier de configuration d'un routeur (configure les interfaces, le protocol de routage interne et BGP)
    - Script main qui génère les fichiers de configuration de tous les AS décrits dans le fichier d'intention et les déplace dans le bon dossier


# Prérequis avant d'exécuter main.py
1. Installez Python
2. Clonez le projet grâce à la commande :
```sh
git clone https://github.com/Marine600/GNS_project.git
```
3. Il faut avoir installé le logiciel GNS3 et avoir déjà créé un projet où tous les routeurs ont été créés et connectés entre eux. Pour savoir quels interfaces connecter entre elles, adaptez le fichier _GNS.json_ à votre réseau, puis tapez dans le terminal la commande suivante :
```sh
python3 plan_config.py
```
4. Une fois les routeurs créés, allez dans main.py et remplissez le dictionnaire dico_correp avec le nom de votre routeur, le nom de son dossier dans les dynamips de GNS3 et le numéro de l'image du routeur
5. Adaptez également le chemin de votre dossier _project-files_ dans lequel se trouvent les dossiers de vos routeurs dans le fichier _drag_and_drop.py_


# Exécution du programme
Exécutez le programme grâce à la commande suivante :
```sh
python3 main.py
```

