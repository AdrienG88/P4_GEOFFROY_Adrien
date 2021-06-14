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

Dans la console, entrez la commande suivante pour exécuter le programme :

      python centreechecsprogramme.py

Ce script va créer une base de données si besoin et exécuter la boucle principale du contrôleur.

2.  Une fois exécuté, vous devez ajouter au minimum 8 joueurs.

3.  Créez ensuite un tournoi.

4.  Sélectionnez les joueurs à importer.

Voilà, vous pouvez à présent, ajouter de nouvelles rondes à votre tournoi!


## Mode d'emploi de flake8

1. flake8 ne nécessite pas d'installation supplémentaire étant donné que son installation s'effectue en même temps que le reste de l'environnement virtuel.


2. Dans la console, entrez successivement les commandes suivantes:

      a.

            mkdir flake8_reports

      pour créer le dossier qui contiendra les rapports.


      b.

            flake8 --max-line-length=119 --outputfile=/flake8_reports/report.html centreechecsprogramme.py

            flake8 --max-line-length=119 --outputfile=/flake8_reports/report.html P4_01_model.py

            flake8 --max-line-length=119 --outputfile=/flake8_reports/report.html P4_02_view.py

            flake8 --max-line-length=119 --outputfile=/flake8_reports/report.html P4_03_controller.py

afin de générer un rapport d'erreurs contenu dans le dossier flake8-reports qui aura analysé les 4 fichiers du projet. 


