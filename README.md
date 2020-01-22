# airbnb
## prérequis
* Python 3.X.Y
* [Pip](https://packaging.python.org/tutorials/installing-packages/) compatible avec Python 3.X.Y

## installation
Le fichier de configuration de base de donnée est : `src/config/db.json`. Ce dernier doit contenir un accès à la base de données, qui doit être créé et populée via les scripts de création (`airbnb-schema.sql` et `airbnb-data.sql`).
Il en est de même avec les vues, les triggers, les procédures ainsi que les fonctions qui doivent être exécutés avant de pouvoir utiliser l'application.

Les instructions suivantes s'effectuent dans un invite de commande de type bash.
Pour commencez, aller dans le dossier `src/`:
```
cd src
```
L'installation des dépendance se fait via le gestionnaire de dépendances pip via la commande suivante.
```
pip3 install -r requirements.txt
```

Puis, pour lancer l'application il suffit d'exécuter le script `gui.py`.
```
python3 gui.py
```

Il faut ensuite utiliser les flèches du clavier ainsi que enter pour naviguer dans l'application.
Pour revenir en arrière dans l'application, il suffit d'utiliser Ctrl+C.

En cas de problème avec l'installation ou de questions, n'hésitez pas à nous contacter par email.
