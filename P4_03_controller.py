# IMPORTATIONS
from P4_01_model import Player, Tournament, Round, Test
from P4_02_view import *
from tinydb import TinyDB, Query

# DECLARATION DE VARIABLES PREALABLE
player_list = list()


class Controller:
    def __init__(self):
        self.db = TinyDB('db.json')

        self.view = View()

        self.tournament = Tournament(str(), int(), list(), list())
        self.player = Player(str(), int())
        self.round = Round(str(), list())
        self.test = Test()

    def main_loop(self):
        length = 5
        while True:
            selection = self.view.display_main_menu()

            if selection == '1':
                # Menu creation
                self.creation_loop()

            if selection == '2':
                # Menu tournoi
                self.tournament_loop()

            if selection == '3':
                # Menu recherche
                self.search_loop()

            if selection == '4':
                # Menu rapports
                self.reports_loop()

            if selection == '5':
                # Quitter le programme
                break

            else:
                self.view.display_menu_options(length)

    def creation_loop(self):
        length = 3
        while True:
            selection = self.view.display_creation_menu()

            if selection == '1':
                # Ajouter un tournoi
                # Creation de l'instance de classe Tournament
                t_name = self.view.input_t_name()
                t_rounds_nr = self.view.input_t_rounds_nr()
                tournament = self.tournament.create_tournament(t_name, t_rounds_nr)
                # Serialisation
                serialized_tournament = self.tournament.serialize_tournament(tournament)
                # Stockage dans db
                self.tournament.save_tournament(serialized_tournament)
                # TEST input vs db
                created_tournament = self.tournament.get_created_tournament(db)
                self.test.test_created_tournament(tournament, created_tournament)

            if selection == '2':
                # Ajouter un joueur
                # Creation de l'instance de classe Player
                name = self.view.input_p_name()
                elo = self.view.input_p_elo()
                player = self.player.create_player(name, elo)
                # Serialisation
                serialized_player = self.player.serialize_player(player)
                # Stockage dans db
                self.player.save_player(serialized_player)
                # TEST input vs db
                created_player = self.player.get_created_player(db)
                self.test.test_created_player(player, created_player)

            if selection == '3':
                # Menu principal
                break

            else:
                self.view.display_menu_options(length)

    def tournament_loop(self):
        # defining all options available in tournament menu
        length = 3
        while True:
            selection = self.view.display_tournament_menu()

            if selection == '1':
                # CHARGER LE TOURNOI
                pass

            if selection == '2':
                # AJOUTER UNE RONDE
                # verifier que le tournoi actif est le bon
                # comparer le nombre de rondes enregistrees avec le nombre de rondes total
                # lancer le script de rondes
                pass

            if selection == '3':
                break

            else:
                self.view.display_menu_options(length)

    def search_loop(self):
        # defining all options available in tournament menu
        length = 3
        while True:
            selection = self.view.display_search_menu()

            if selection == '1':
                # Rechercher un joueur
                pass

            if selection == '2':
                # Rechercher un tournoi
                pass

            if selection == '3':
                break

            else:
                self.view.display_menu_options(length)

    def reports_loop(self):
        length = 6
        while True:
            selection = self.view.display_reports_menu()

            if selection == '1':
                # Liste de tous les acteurs
                pass

            if selection == '2':
                # Liste de tous les joueurs d\'un tournoi
                self.view.display_player_list()

            if selection == '3':
                # Liste de tous les tournois
                self.view.display_tournament_list()

            if selection == '4':
                # Liste de toutes les rondes d\'un tournoi
                pass

            if selection == '5':
                # Liste de tous les matchs d\'un tournoi
                pass

            if selection == '6':
                # Menu principal
                break

            else:
                self.view.display_menu_options(length)
