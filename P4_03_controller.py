# IMPORTATIONS
from P4_01_model import Player, Tournament, Round, Match, Test, Serializer
from P4_02_view import *
from tinydb import TinyDB, Query

# DECLARATION DE VARIABLES PREALABLE
players_table = db.table('players')
tournaments_table = db.table('tournaments')


class Controller:
    def __init__(self):
        self.db = TinyDB('db.json')
        self.view = View()
        self.tournament = Tournament(str(), int(), list(), list())
        self.player = Player(str(), int())
        self.round = Round(str(), list())
        self.match = Match(Player(str(), int()), Player(str(), int()), float(), float())
        self.test = Test()
        self.serializer = Serializer()

# METHODES DU CONTROLEUR
    def create_tournament(self):
        # Ajouter un tournoi
        # Creation de l'instance de classe Tournament
        tour_name = self.view.input_tour_name()
        tour_rounds_nr = self.view.input_tour_rounds_nr()
        tournament = self.tournament.create_tournament(tour_name, tour_rounds_nr)
        # Serialisation
        serialized_tournament = self.tournament.serialize_tournament(tournament)
        # Stockage dans db
        Tournament.save_tournament(serialized_tournament, db)
        # désérialise le tournoi créé/stocké sur la db pour test
        created_tournament = self.tournament.get_created_tournament(db)
        # TEST input vs db
        self.test.test_created_tournament(tournament, created_tournament)

    def create_player(self):
        # Ajouter un joueur
        # Creation de l'instance de classe Player
        player_name = self.view.input_player_name()
        player_elo = self.view.input_player_elo()
        player = self.player.create_player(player_name, player_elo)
        # Serialisation
        serialized_player = self.player.serialize_player(player)
        # Stockage dans db
        self.player.save_player(serialized_player)
        # TEST input vs db
        created_player = self.player.get_created_player(db)
        self.test.test_created_player(player, created_player)

    # BOUCLES DU MENU

    def main_loop(self):
        loop_length = 5
        while True:
            user_selection = self.view.display_main_menu()

            if user_selection == '1':
                # Menu creation
                self.creation_loop()

            if user_selection == '2':
                # Menu tournoi
                self.tournament_loop()

            if user_selection == '3':
                # Menu recherche
                self.search_loop()

            if user_selection == '4':
                # Menu rapports
                self.reports_loop()

            if user_selection == '5':
                # Quitter le programme
                break

            else:
                self.view.display_menu_options(loop_length)

    def creation_loop(self):
        loop_length = 4
        while True:
            user_selection = self.view.display_creation_menu()

            if user_selection == '1':
                self.create_tournament()

            if user_selection == '2':
                self.create_player()

            if user_selection == '3':
                # Ajouter les joueurs au tournoi
                # player_list = self.player.get_players_from_db()
                # print(player_list)
                # self.tournament.add_players_to_tournament(player_list)
                pass

            if user_selection == '4':
                # Menu principal
                break

            else:
                self.view.display_menu_options(loop_length)

    def tournament_loop(self):
        # defining all options available in tournament menu #modifier
        loop_length = 4
        while True:
            #user_choice
            user_selection = self.view.display_tournament_menu()

            if user_selection == '1':
                # CHARGER LE TOURNOI
                # Rechercher le tournoi par nom
                # Fonction de saisie du nom
                tour_name = self.view.input_tour_name()
                # Recuperation du tournoi selectionné dans la db
                tournament = self.tournament.get_tournament(tour_name, db)
                # Deserialisation du tournoi en instance de classe Tournament
                active_tournament = self.tournament.deserialize_tournament(tournament)
                # On retourne le tournoi actif pour le manipuler par la suite
                return active_tournament

            if user_selection == '2':
                # AJOUTER UNE RONDE
                # verifier que le tournoi actif est le bon
                # Fonction de saisie du nom
                tour_name = self.view.input_tour_name()
                # Recuperation du tournoi selectionné dans la db
                tournament = self.tournament.get_tournament(tour_name, db)
                # Deserialisation du tournoi en instance de classe Tournament
                active_tournament = self.tournament.deserialize_tournament(tournament)
                # Deserialisation du classement
                active_tournament.player_ratings =\
                    self.tournament.deserialize_player_ratings(active_tournament)
                # comparer le nombre de rondes enregistrees avec le nombre total de rondes

                # Lancer le script de rondes
                player_ratings = active_tournament.player_ratings
                # Premiere ronde
                #methode
                if len(active_tournament.rounds) == 0:
                    # classer les joueurs en fonction de leur ELO et résultat
                    self.tournament.sort_players(player_ratings)
                    # afficher le classement du tournoi
                    self.view.display_player_ratings(player_ratings)
                    # afficher les matches de la ronde
                    # créer une liste jumelle du classement des joueurs pour créer les matches de la ronde
                    tmp_round_players = list()
                    for player in player_ratings:
                        tmp_round_players.append(player)
                    # ordonner la liste en fonction des matches de la ronde
                    self.round.create_round1_matches(tmp_round_players)
                    self.view.display_round_matches(tmp_round_players)
                    # entrer les résultats de la ronde 1
                    matches = list()
                    for i in range(0, len(tmp_round_players), 2):
                        self.view.input_round_matches(i, tmp_round_players)
                        score_w = self.view.input_player_score_white()
                        score_b = self.view.input_player_score_black()
                        match = Match(tmp_round_players[i][0], tmp_round_players[i+1][0], score_w, score_b)
                        matches.append(match)

                    for match in matches:
                        print(match.player_white[0].name, match.player_white[0].elo, match.player_white[1],
                              match.player_black[0].name, match.player_black[0].elo, match.player_black[1])

                    # create_round
                    first_round = Round('round1', matches)
                    # serialize_matches
                    self.serializer.serialize_round(first_round)

                # elif len(active_tournament.rounds) < active_tournament.rounds_nr
#                else:
#                    break

            if user_selection == '3':
                # Ajouter les joueurs au tournoi
                # Recuperer les joueurs dans la db
                players_list = db.table('players').all()
                # Afficher le nombre de joueurs importés
                self.view.display_players_list_length(players_list)
                # Saisir le nom du tournoi à traiter
                name = self.view.input_tour_name()
                # Recuperer le tournoi selectionné dans la db
                tournament = self.tournament.get_tournament(name, db)
                # Deserialiser le tournoi en instance de classe Tournament
                active_tournament = self.tournament.deserialize_tournament(tournament)
                # Transformer les joueurs {"Nom": name, "ELO": elo} en tuples ({"Nom": name, "ELO": elo}, score=0)
                rated_players = list()
                for player in players_list:
                    rated_player = self.player.create_rated_player(player, 0)
                    rated_players.append(rated_player)
                # Modifier l'attribut players du tournoi
                active_tournament.players = rated_players
                # Serialiser le tournoi pour exportation dans db
                active_tournament = self.tournament.serialize_tournament(active_tournament)
                # Effacer l'ancienne version du tournoi dans la db
                self.tournament.erase_tournament(active_tournament, db)
                # Enregistrer les modifications dans la db
                Tournament.save_tournament(active_tournament, db)

            if user_selection == '4':
                break

            else:
                self.view.display_menu_options(loop_length)

    def search_loop(self):
        # defining all options available in tournament menu
        loop_length = 3
        while True:
            user_selection = self.view.display_search_menu()

            if user_selection == '1':
                # Rechercher un joueur
                name = self.view.input_player_name()
                self.view.search_player_by_name(players_table, name)

            if user_selection == '2':
                # Rechercher un tournoi
                name = self.view.input_tour_name()
                self.view.search_tournament_by_name(tournaments_table, name)

            if user_selection == '3':
                break

            else:
                self.view.display_menu_options(loop_length)

    def reports_loop(self):
        loop_length = 6
        while True:
            user_selection = self.view.display_reports_menu()

            if user_selection == '1':
                # Liste de tous les acteurs
                pass

            if user_selection == '2':
                # Liste de tous les joueurs d\'un tournoi
                self.view.display_player_list()

            if user_selection == '3':
                # Liste de tous les tournois
                self.view.display_tournament_list()

            if user_selection == '4':
                # Liste de toutes les rondes d\'un tournoi
                pass

            if user_selection == '5':
                # Liste de tous les matchs d\'un tournoi
                pass

            if user_selection == '6':
                # Menu principal
                break

            else:
                self.view.display_menu_options(loop_length)
