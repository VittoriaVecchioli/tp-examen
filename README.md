# tp-examen

## Notes: 

## Exercice1 :
L'objectif de cet exercice est de lancer 3 groupes de conteneurs contenant à la fois un reverse proxy Nginx, un conteneur en charge de l'interprétation des fichiers PHP et une base de données pour stocker des données. 

Un reverse proxy sera également présent pour rediriger les conteneurs vers chacune des stacks. 

Pour cela, nous allons utiliser un fichier docker-compose permettant de regrouper les différents sites. 

* ***Question 1.A*** : 

Créez un premier fichier docker-compose_q1 composé d'un service nommé ***web***, Un service de base de données ***postgresql*** et un service ***php***. 

Les conteneurs porteront le même nom que les services définis précédemment . 

On utilisera respectivement les images docker nginx, postgres version 10 et pichouk/php (qui contient les bibliothèque php postgresql pour fonctionner avec la base de données). 

Vous utiliserez des volumes pour monter les fichiers de configuration dans les conteneurs et pour partager les fichiers PHP entre le conteneur Nginx et le conteneur PHP-FPM ainsi pour persister les données de votre database postgres. 

Les conteneurs utiliseront un network appelé backend et le conteneur nginx exposera son port 80 sur le port 80 de votre hôte docker . 

Le service web dependra du service postgresql . 

Ci-dessous du fichier index.php appelant la base de données : 

```
#exercice1/html/index.php
<?php
    echo "<h1>Trois commandes très utiles sur Docker</h1></br>";
    echo "<ol>";
    $connexion = new PDO('pgsql:host=postgresql;port=5432;dbname=database', 'admin', 'dauphine');
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
#exercice1/nginx/site1.conf
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

Vous devez egalement inserer les commandes suivantes ***manuellement*** dans votre database, les commandes seront affichées dans votre page web : 

docker ps - docker run - docker container prune 

l'arboresence pour la 1ere question: 

```
excerice1
├── bdd
│   └── data1
│
├── docker-compose_q1.yml
├── html
│   └── index.php
└── nginx
    └── site1.conf
```

vous devez associer le dossier /html de votre machine hote avec le dossier /usr/share/nginx/html du conteneur web, mettre le fichier site1.conf dans le repertoire /etc/nginx/conf.d/ en le renommant à default.conf du conteneur web, associer le dossier /html de votre machine hote avec le dossier /usr/share/nginx/html du conteneur php, et associer le dossier /data1 de votre machine au repertoire /var/lib/postgresql/data du conteneur postgresql. 

* ***Question 1.B*** : 

A partir d'une image Nginx, nous allons maintenant passer par un service proxy qui sera en charge de faire reverse proxy vers notre application. 

Celui-ci se trouvera dans un réseau appelé front , on exposera le port 80 du conteneur proxy sur le port 80 de la machine hote docker. 

L'idée est de rediriger toutes les requêtes provenant du nom de domaine monsite1.fr vers notre conteneur appelé web. 

Notre conteneur Nginx applicatif du service web n'a plus besoin d'exposer son port sur l'hôte Docker, c'est le reverse proxy qui va s'en charger. 

Là encore nous allons devoir monter un fichier de configuration pour nginx afin de lui indiquer vers quel conteneur il faut rediriger les requêtes provenant d'un nom de domaine. 

```
exercice1/nginx/proxy.conf
server {
	listen 80;
	server_name monsite1.fr;
	location / {
        proxy_pass http://web:80;
    }
}
```

Votre fichier docker-compose sera nommé "docker-compose_q2" . 

***Astuce*** : vous pouvez utiliser le docker-compose_q1 comme support, il faudra cepandant ajouter le fichier proxy.conf dans le repertoire /etc/nginx/conf.d/ en le renommant default.conf pour le service proxy 

* ***Question 2*** : 

Nous allons maintenant ajouter une seconde application. Celle-ci sera elle aussi composée d'un conteneur Nginx, d'un conteneur PHP-FPM et d'une base de données PostgreSQL indépendante. 

Les conteneurs de cette nouvelle application vont se trouver dans un network séparé de la première application qui sera appelé backend2. 

Notre fichier index.php a été mis à jour pour notre nouvelle application.

```
exercice1/html2/index.php
<?php
    echo "<h1>Trois commandes très utiles sur docker v2</h1></br>";
    echo "<ol>";
    $connexion = new PDO('pgsql:host=postgresql;port=5432;dbname=database', 'admin', 'dauphine');
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
