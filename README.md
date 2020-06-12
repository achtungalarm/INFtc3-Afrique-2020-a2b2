 base-de-données
# INFtc3-Afrique-2020-a2b

Projet Web INF tc3 du groupe A2B qui a choisi le projet : l'Afrique

Ces contributeurs sont :

- Allan B (AchtungAlarm)
- Fabien D
- Cristina L
- Naomi S
- Clément S

## Le but de ce projet

Nous devons créer un serveur web qui devra présenter le continent africain, ses pays et diverses informations à travers une interface web.

## Partie base de données

Pour avoir les informations nécessaire à afficher, il faut que celles ci soient uniformisées et standardisées. Pour se faire, nous diposions d'un fichier .zip regroupant une grande majorité d'informations au format .json directement issues de Wikipédia grâce à la librairie wptools sous Python. Les données n'étant pas standardisées, il a fallu essayer de créer des expressions régulières pouvant extraire au mieux les données. Si les informations n'apparaissent pas dans les fichiers .json, on essaye d'automatiser une recherche Wikipédia qui permettrait d'accéder à ces données.

La version du 05/06/20 de notre fichier Python extrait les noms officiels, les capitales ainsi que ses coordonnées longitute et latitude (nombre réel positif ou négatif) pour les enregistrer dans une base de données avec la librairie squlite3. Les données étant incomplètes, le processus a besoin de 6 recherches internet pour collecter toutes ces données concernant les 54 pays d'Afrique.

La version du 12/06/20 de notre code règle le problème concernant la maladroite confusion entre longitude et latitude et permet désormais de sauvergarder un pays déjà existant en l'éditant. Il s'avère que la recherche sur les coordonnées de certaines capitales (Dodoma) n'aboutit pas. Il faut donc aller la chercher à la main et la rentrer dans la base de données avec la commande edit_country.
=======
INFtc3-Afrique-2020-a2b

Projet Web INF tc3 du groupe A2B qui a choisi le projet : l'Afrique

Ces contributeurs sont :

    Allan B (AchtungAlarm)
    Fabien D
    Cristina L
    Naomi S
    Clément S

Le but de ce projet

Nous devons créer un serveur web qui devra présenter le continent africain, ses pays et diverses informations à travers une interface web.
Partie base de données

Pour avoir les informations nécessaire à afficher, il faut que celles ci soient uniformisées et standardisées. Pour se faire, nous diposions d'un fichier .zip regroupant une grande majorité d'informations au format .json directement issues de Wikipédia grâce à la librairie wptools sous Python. Les données n'étant pas standardisées, il a fallu essayer de créer des expressions régulières pouvant extraire au mieux les données. Si les informations n'apparaissent pas dans les fichiers .json, on essaye d'automatiser une recherche Wikipédia qui permettrait d'accéder à ces données.

La version du 05/06/20 de notre fichier Python extrait les noms officiels, les capitales ainsi que ses coordonnées longitute et latitude (nombre réel positif ou négatif) pour les enregistrer dans une base de données avec la librairie squlite3. Les données étant incomplètes, le processus a besoin de 6 recherches internet pour collecter toutes ces données concernant les 54 pays d'Afrique.

La version du 12/06/20 de notre code règle le problème concernant la maladroite confusion entre longitude et latitude et permet désormais de sauvergarder un pays déjà existant en l'éditant. Il s'avère que la recherche sur les coordonnées de certaines capitales (Dodoma) n'aboutit pas. Il faut donc aller la chercher à la main et la rentrer dans la base de données avec la commande edit_country.

