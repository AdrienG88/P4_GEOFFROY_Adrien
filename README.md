# P4 Python Software for OpenClassrooms


## Contenu du projet:

1 fichier requirements.txt

3 fichiers Python contenant le code-source du programme

1 fichier exécutable centreechecsprogramme.py à exécuter

1 fichier README.me contenant la marche à suivre pour faire fonctionner le programme.


## Installation de l'environnement virtuel

1.  Pour créer l'environnement virtuel nécessaire au fonctionnement des scripts:

      a.Entrez la commande suivante dans la console pour créer un environnement virtuel à partir du module venv:
      
        python -m venv <nom-souhaité-de-l-environnement>
      
      
      b.Grâce à la commande suivante, activez l'environnement virtuel (sous Windows):
      
        <nom-souhaité-de-l-environnement>\Scripts\activate.bat
        
        
      c.Entrez la commande suivante dans la console pour installer les modules et paquets nécessaires dans l'environnement virtuel actif:
      
        pip install -r requirements.txt

## Mode d'emploi du programme:

1.  Exécutez le script centreechecsprogramme.py avec Python

Dans la console, entrez la commande suivante pour exécuter le programme:

      python centreechecsprogramme.py

Ce script va créer une base de données si besoin et exécuter la boucle principale du contrôleur.

2.  Une fois exécuté, vous devez ajouter au minimum 8 joueurs.

3.  Créez ensuite un tournoi.

4.  Sélectionnez les joueurs à importer.

Voilà, vous pouvez à présent, ajouter de nouvelles rondes à votre tournoi!


## Mode d'emploi de flake8

1. Décompresser l'archive flake8.zip contenant un dossier flake8, lui-même contenant un fichier tox.ini dans le dossier du projet.


2. Dans la console, entrez la commande suivante:

       flake8 --config=flake8/tox.ini --output-file=flake8/flake8-report.html

afin de générer un rapport d'erreurs contenu dans le dossier flake8 qui aura analysé les 4 fichiers du projet.
