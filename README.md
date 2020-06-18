# INFtc3-Afrique-2020-a2b

Projet Web INF tc3 du groupe A2B qui a choisi le projet : l'Afrique

Ces contributeurs sont :

- Allan B (achtungalarm)
- Fabien D (fabiendupuis)
- Cristina L (cristinalopez4)
- Naomi S (atewdrew)
- Clément S (clement-sautiere)

tous droits réservés.  Test

## Le but de ce projet

Nous devons créer un serveur web qui devra présenter le continent africain, ses pays et diverses informations à travers une interface web. 

## Partie base de données

Pour avoir les informations nécessaire à afficher, il faut que celles ci soient uniformisées et standardisées. Pour se faire, nous diposions d'un fichier .zip regroupant une grande majorité d'informations au format .json directement issues de Wikipédia grâce à la librairie wptools sous Python. Les données n'étant pas standardisées, il a fallu essayer de créer des expressions régulières pouvant extraire au mieux les données. Si les informations n'apparaissent pas dans les fichiers .json, on essaye d'automatiser une recherche Wikipédia qui permettrait d'accéder à ces données.

La version du 05/06/20 de notre fichier Python extrait les noms officiels, les capitales ainsi que ses coordonnées longitute et latitude (nombre réel positif ou négatif) pour les enregistrer dans une base de données avec la librairie squlite3. Les données étant incomplètes, le processus a besoin de 6 recherches internet pour collecter toutes ces données concernant les 54 pays d'Afrique.

La version du 12/06/20 de notre code règle le problème concernant la maladroite confusion entre longitude et latitude et permet désormais de sauvergarder un pays déjà existant en l'éditant. Il s'avère que la recherche sur les coordonnées de certaines capitales (Dodoma) n'aboutit pas. Il faut donc aller la chercher à la main et la rentrer dans la base de données avec la commande edit_country.

## Partie serveur

Nous sommes parti d'un exemple vu en travaux dirigés qui utilisait un fichier javascript pour mettre en place un environnement Leaflet, qui est une solution pour avoir une map glissante. Nous disposions donc d'un fichier .html, .js et .css pour que l'on puisse s'occuper de l'affichage, ainsi que d'un fichier .py pour avoir un serveur par défaut. Nous avons donc adapté ces fichiers pour qu'ils répondent à notre cahier des charges. 

La première fonction que nous avons ajouté à notre programme python est l'envoie des coordonnées au fichier .html pour pouvoir placer les pointeurs (/location). Il nous a ensuite fallu dire au fichier .html de placer un marqueur aux coordonnées indiquées.

La deuxième foncitonnalité que nous avons ajouté au programme python est l'envoie des données au fichier .html, lorsque ce dernier en a besoin (/description). Il nous a ensuite fallu dire au fichier .html d'ajouter une méthode au marqueur qui s'exécute quand on clique dessus (ce sont des commandes JavaScript, mais dans le fichier .html entre les balises <script>). Quand le clique est réalisé, on demande au serveur d'accéder à /desription, il va donc nous retourner les données du pays concerné. Il nous suffit de les afficher grâce au fichier html.
  
Nous disposions déjà des drapeaux de chacun des pays dont le nom était : nom-largeurxhauteur.png qui se situent dans le répertoire /flags. Ainsi nous avons ajouter dans la deuxième fonctionnalité l'aperçu du drapeau sur la page web.

Quelques petits détails : un environnement colonne a été ajouté pour un affichage plus esthétique, la map a été agrandie en hauteur pour une meilleure visibilité, le niveau de zoom et la position par défaut a été revue pour englober tout le continent, un zoom automatique et un centrage est effectué quand on clique sur un pointeur (non adapté à la dimension du pays).
