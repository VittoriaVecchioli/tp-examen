# tp-examen

## Notes: 

## Exercice1 :
L'objectif de cet exercice est de lancer 3 groupes de conteneurs contenant à la fois un reverse proxy Nginx, un conteneur en charge de l'interprétation des fichiers PHP et une base de données pour stocker des données. 

Un reverse proxy sera également présent pour rediriger les conteneurs vers chacune des stacks. 

Pour cela, nous allons utiliser un fichier docker-compose permettant de regrouper les différents sites. 

* ***Question 1*** : 

Créez un premier fichier docker-compose_q1 composé d'un service nommé Web, Un service de base de données PostgresSQL et un service PHP. 

Les conteneurs porteront le même nom que les services définis précédemment . 

On utilisera respectivement les images docker nginx, postgres version 10 et pichouk/php (qui contient les bibliothèque php postgresql pour fonctionner avec la base de données). 

Vous utiliserez des volumes pour monter les fichiers de configuration dans les conteneurs et pour partager les fichiers PHP entre le conteneur Nginx et le conteneur PHP-FPM ainsi pour persister les données de votre database postgres. 

Les conteneurs utiliseront un network appelé backend et le conteneur nginx exposera son port 80 sur le port 80 de votre hôte docker .

Ci-dessous un example de fichier PHP appelant la base de données : 

```
exercice1/html/index.php
<?php
    echo "<h1>Trois commandes très utiles sur Docker</h1></br>";
    echo "<ol>";
    $connexion = new PDO('pgsql:host=postgresql;port=5432;dbname=database', 'postgresql', 'dauphine');
    $sql = 'SELECT data FROM commande';
    $results = $connexion->prepare($sql);
    $results->execute();
    while ($row = $results->fetch(PDO::FETCH_ASSOC)){
        echo "<li><b>" . $row['data'] . "</b> : ";
        echo $row['def'] . "</li>";
    }
    echo "</ol>";
?>
```

Vous devez créer un fichier de configuration Nginx qui va lire un fichier d'index PHP et demander son traitement à votre conteneur PHP. 

```
exercice1/nginx/site1.conf
server{
        listen 80;

        server_name _;
        root /usr/share/nginx/html;
        index index.php index.html;

        location / {
                try_files $uri $uri/ =404;
        }


        location ~ \.php$ {
          try_files $uri =404;
          fastcgi_split_path_info ^(.+\.php)(/.+)$;
          fastcgi_pass php:9000;
          fastcgi_index index.php;
          include fastcgi_params;
          fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
          fastcgi_param PATH_INFO $fastcgi_path_info;
        }

}
```

Vous devez egalement inserer les commandes suivantes ***manuellement*** dans votre table "commande" : 

docker ps / docker run / docker container prune 


le résultat final est : 

* ***Question 2*** : 

A partir d'une image Nginx, nous allons maintenant passer par un service proxy qui sera en charge de faire reverse proxy vers notre application. Celui-ci se trouvera dans un réseau appelé front , on exposera le port 80 du conteneur proxy sur le port 80 de la machine hote docker, le port du conteneur web ne sera donc plus exposé, le fichier docker compose sera nommé "docker-compose_q2" . 

* ***Question 3*** : 

Nous allons maintenant ajouter une seconde application. Celle-ci sera elle aussi composée d'un conteneur Nginx, d'un conteneur PHP-FPM et d'une base de données PostgreSQL indépendante. 

Créez les fichiers de configuration correspondante et mettez à jour le docker-compose.yml pour prendre en compte ce nouveau site. 

Les conteneurs de cette nouvelle application vont se trouver dans un network séparé de la première application qui sera appelé backend2. 

Notre fichier index.php a été mis à jour pour notre nouvelle application. On notera que l'URL de la base de données a été mise à jour pour utiliser une autre base de données que celle de notre première application. 

```
exercice1/html2/index.php
<?php
    echo "<h1>Dix commandes très utiles sur Ubuntu v2</h1></br>";
    echo "<ol>";
    $connexion = new PDO('pgsql:host=postgresql2;port=5432;dbname=prism', 'snowden', 'nsa');
    $sql = 'SELECT * FROM commande';
    $results = $connexion->prepare($sql);
    $results->execute();
    while ($row = $results->fetch(PDO::FETCH_ASSOC)){
        echo "<li><b>" . $row['com'] . "</b> : ";
        echo $row['def'] . "</li>";
    }
    echo "</ol>";
?>
```
Vous devez créer un fichier de configuration Nginx qui va lire un fichier d'index PHP et demander son traitement à votre conteneur PHP. Cette fois-ci, nous allons changer de serveur PHP en modifiant la ligne fastcgi_pass .

```
exercice1/nginx/site2.conf
server{
        listen 80;

        server_name _;
        root /usr/share/nginx/html;
        index index.php index.html;

        location / {
                try_files $uri $uri/ =404;
        }


        location ~ \.php$ {
          try_files $uri =404;
          fastcgi_split_path_info ^(.+\.php)(/.+)$;
          fastcgi_pass php2:9000;
          fastcgi_index index.php;
          include fastcgi_params;
          fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
          fastcgi_param PATH_INFO $fastcgi_path_info;
        }

}
```
Nous devons également ajouter une nouvelle entrée à notre reverse proxy. Les clients arrivant avec l'url http://monsite2.fr seront alors redirigés vers notre nouvelle application (hébergée dans le conteneur web2) tout en laissant la première application fonctionner normalement. 
```
server {
	listen 80;
	server_name monsite1.fr;
	location / {
        proxy_pass http://web:80;
    }
}
server {
	listen 80;
	server_name monsite2.fr;
	location / {
        proxy_pass http://web2:80;
    }
}
```
