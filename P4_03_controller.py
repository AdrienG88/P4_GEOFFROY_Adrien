# IMPORTATIONS
from P4_01_model import Player, Tournament, Round, Match, Test, Deserializer, Serializer
from P4_02_view import *
from tinydb import TinyDB, Query

# DECLARATION DE VARIABLES PREALABLE
players_table = db.table('players')
tournaments_table = db.table('tournaments')


class Controller:
    def __init__(self):
        self.db = TinyDB('db.json')
        self.view = View()
        self.tournament = Tournament(str(), list(), int(), list(), list())
        self.player = Player(str(), int())
        self.round = Round(str(), list())
        self.match = Match(Player(str(), int()), Player(str(), int()), float(), float())
        self.test = Test()
        self.deserializer = Deserializer()
        self.serializer = Serializer()

# METHODES DU CONTROLEUR
    def create_tournament(self):
        tour_name = self.view.input_tour_name()
        tour_rounds_nr = self.view.input_tour_rounds_nr()
        tournament = self.tournament.create_tournament(tour_name, tour_rounds_nr)
        serialized_tournament = self.serializer.serialize_tournament(tournament)
        self.tournament.save_tournament(serialized_tournament, db)
        created_tournament = self.tournament.get_created_tournament(db)
        self.test.test_created_tournament(tournament, created_tournament)

    def create_player(self):
        player_name = self.view.input_player_name()
        player_elo = self.view.input_player_elo()
        player = Player(name=player_name, elo=player_elo)
        serialized_player = self.serializer.serialize_player(player)
        self.player.save_player(serialized_player)
        created_player = self.player.get_created_player(db)
        self.test.test_created_player(player, created_player)

    def delete_player(self):
        name = self.view.input_player_name()
        player = players_table.search(Query().Nom == name)
        print(player)
        user_choice = self.view.input_user_choice_deletion()
        if user_choice == 'Y':
            players_table.remove(Query().Nom == name)
            print('Suppression effectuée')
        if user_choice == 'N':
            print('Opération annulée')

    def create_players_id_list(self):
        print(db.table('players').all())
        players_id_list = list()
        while len(players_id_list) < 8:
            player_name = self.view.input_player_name()
            self.view.search_player_by_name(players_table, player_name)
            user_choice = self.view.input_user_choice_addition()
            if user_choice == 'Y':
                player_id = players_table.get(Query().Nom == player_name).doc_id
                players_id_list.append(player_id)
            if user_choice == 'N':
                self.view.input_user_choice_import()
                if user_choice == 'Y':
                    pass
                if user_choice == 'N':
                    break
            self.view.display_players_list_length(players_id_list)
            self.view.display_imported_players(players_id_list)
        return players_id_list

    def import_players_to_tournament(self):
        players_id_list = self.create_players_id_list()
        tour_name = self.view.input_tour_name()
        tournament = self.tournament.get_saved_tournament(tour_name, db)
        active_tournament = self.deserializer.deserialize_tournament(tournament)

        player_ratings = list()
        for player_id in players_id_list:
            rated_player = [player_id, 0]
            player_ratings.append(rated_player)
        active_tournament.player_ratings = player_ratings
        serialized_tournament = self.serializer.serialize_tournament(active_tournament)
        self.tournament.save_tournament(serialized_tournament, db)

    def import_tournament(self):
        tour_name = self.view.input_tour_name()
        tournament = self.tournament.get_saved_tournament(tour_name, db)
        active_tournament = self.deserializer.deserialize_tournament(tournament)
        return active_tournament

    @staticmethod
    def create_matchmaking_data(player_ratings):
        matchmaking_data = list()
        for i in range(0, len(player_ratings), 2):
            played_match = player_ratings[i][0], player_ratings[i + 1][0]
            matchmaking_data.append(played_match)
        return matchmaking_data

    def create_round_matches(self, player_ratings):
        matches = list()
        for i in range(0, len(player_ratings), 2):
            self.view.input_round_results(i, player_ratings)
            score_white = self.view.input_player_score_white()
            score_black = self.view.input_player_score_black()
            player_white = self.deserializer.deserialize_player(players_table.get(doc_id=player_ratings[i][0]))
            player_black = self.deserializer.deserialize_player(players_table.get(doc_id=player_ratings[i+1][0]))
            player_ratings[i][1] += float(score_white)
            player_ratings[i+1][1] += float(score_black)
            match = Match(player_white, player_black, score_white, score_black)
            matches.append(match)
        return matches

    def create_first_round(self, player_ratings, active_tournament):
        self.tournament.sort_players(player_ratings, players_table)
        self.view.display_player_ratings(player_ratings)
        self.round.pair_round1_matches(player_ratings)
        self.view.display_round_matches(player_ratings)

        new_matchmaking_data = self.create_matchmaking_data(player_ratings)
        for played_match in new_matchmaking_data:
            active_tournament.matchmaking_data.append(played_match)

        round = Round(name='Ronde 1', matches=self.create_round_matches(player_ratings))
        active_tournament.rounds.append(round)

        serialized_tournament = self.serializer.serialize_tournament(active_tournament)

        self.tournament.save_tournament(serialized_tournament, db)

    def create_other_round(self, player_ratings, active_tournament):
        self.tournament.sort_players(player_ratings, players_table)
        self.view.display_player_ratings(player_ratings)
        tested_matchmaking_data = active_tournament.matchmaking_data
        self.round.pair_other_rounds_matches(player_ratings, tested_matchmaking_data)
        self.view.display_round_matches(player_ratings)

        new_matchmaking_data = self.create_matchmaking_data(player_ratings)
        for played_match in new_matchmaking_data:
            active_tournament.matchmaking_data.append(played_match)

        round_name = "Ronde "+str(len(active_tournament.rounds)+1)
        round = Round(name=round_name, matches=self.create_round_matches(player_ratings))
        active_tournament.rounds.append(round)

        serialized_tournament = self.serializer.serialize_tournament(active_tournament)

        self.tournament.save_tournament(serialized_tournament, db)

    # BOUCLES DU MENU
    def main_loop(self):
        loop_length = 4
        while True:
            user_selection = self.view.display_main_menu()

            if user_selection == '1':
                self.creation_loop()

            if user_selection == '2':
                self.search_loop()

            if user_selection == '3':
                self.reports_loop()

            if user_selection == '4':
                break

            else:
                self.view.display_menu_options(loop_length)

    def creation_loop(self):
        loop_length = 5
        while True:
            user_selection = self.view.display_creation_menu()

            if user_selection == '1':
                self.create_tournament()

            if user_selection == '2':
                self.player_subloop()

            if user_selection == '3':
                self.import_players_to_tournament()

            if user_selection == '4':
                active_tournament = self.import_tournament()

                if len(active_tournament.rounds) == 0:
                    self.create_first_round(active_tournament.player_ratings, active_tournament)

                elif len(active_tournament.rounds) < int(active_tournament.rounds_nr):
                    self.create_other_round(active_tournament.player_ratings, active_tournament)

                else:
                    print('\nCe tournoi est terminé!')
                    self.tournament.sort_players(active_tournament.player_ratings, players_table)
                    self.view.display_player_ratings(active_tournament.player_ratings)
                    break

            if user_selection == '5':
                break

            else:
                self.view.display_menu_options(loop_length)

    def player_subloop(self):
        loop_length = 3
        while True:
            user_selection = self.view.display_player_submenu()

            if user_selection == '1':
                self.create_player()
            if user_selection == '2':
                self.delete_player()
            if user_selection == '3':
                break
            else:
                self.view.display_menu_options(loop_length)

    def search_loop(self):
        loop_length = 3
        while True:
            user_selection = self.view.display_search_menu()

            if user_selection == '1':
                name = self.view.input_player_name()
                self.view.search_player_by_name(players_table, name)

            if user_selection == '2':
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
                self.view.display_actor_list()

            if user_selection == '2':
                self.view.display_tournament_player_list()

            if user_selection == '3':
                self.view.display_tournament_list()

            if user_selection == '4':
                self.view.display_all_tournament_rounds()

            if user_selection == '5':
                self.view.display_all_round_matches()

            if user_selection == '6':
                break

            else:
                self.view.display_menu_options(loop_length)
