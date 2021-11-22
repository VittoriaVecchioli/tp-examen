# tp-examen

## Notes: 

## Exercice1 :
L'objectif de cet exercice est de lancer 3 groupes de conteneurs contenant à la fois un reverse proxy Nginx, un conteneur en charge de l'interprétation des fichiers PHP et une base de données pour stocker des données. 

Un reverse proxy sera également présent pour rediriger les conteneurs vers chacune des stacks. 

Pour cela, nous allons utiliser un fichier docker-compose permettant de regrouper les différents sites. 

* Question 1 : 

Créez un premier fichier docker-compose composé d'un conteneur Nginx, d'une base de données PostgresSQL et d'un conteneur PHP-FPM. 

On utilisera respectivement les images docker nginx, postgres et pichouk/php (qui contient les bibliothèque php postgresql pour fonctionner avec la base de données). 

Vous utiliserez des volumes pour monter les fichiers de configuration dans les conteneurs et pour partager les fichiers PHP entre le conteneur Nginx et le conteneur PHP-FPM. 

Les conteneurs utiliseront un network appelé backend et le conteneur nginx exposera son port 80 sur le port 80 de votre hôte docker 
