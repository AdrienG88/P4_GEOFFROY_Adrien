import json
from tinydb import TinyDB, Query

#add serialized_players

# DEFINITION DES CLASSES ET METHODES AFFERENTES


class Player:
    def __init__(self, name, elo):
        self.name = name
        self.elo = elo
        self.db = TinyDB('db.json')

    def create_player(self, name, elo):
        player = Player(name, elo)
        return player

    def serialize_player(self, player):
        serialized_player = {'Nom': player.name, 'ELO': player.elo}
        return serialized_player

    def deserialize_player(self, player):
        name = player['Nom']
        elo = player['ELO']
        deserialized_player = Player(name, elo)
        return deserialized_player

#    def get_players_from_db(self):
#        player_list = list()
#        for player in self.db.table('players'):
#            deserialized_player = self.deserialize_player(player)
#            player_list.append(deserialized_player)
#        return player_list

    def create_rated_player(self, player, score):
        rated_player = (player, score)
        return rated_player

    def save_player(self, serialized_player):
        players_table = self.db.table('players')
        players_table.insert(serialized_player)
        return serialized_player

    def get_created_player(self, db):
        name = db.table('players').all()[-1]['Nom']
        elo = db.table('players').all()[-1]['ELO']
        created_player = Player(name, elo)
        print(created_player.name, created_player.elo)
        return created_player

    def to_json(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__))


class Tournament:
    def __init__(self, name, player_ratings, rounds_nr, rounds):
        self.name = name
        self.player_ratings = player_ratings
        self.rounds_nr = rounds_nr
        self.rounds = rounds
        self.db = TinyDB('db.json')
        self.player = Player(str(), int())

    def create_tournament(self, name, rounds_nr):
        player_ratings = list()
        rounds = list()
        tournament = Tournament(name, player_ratings, rounds_nr, rounds)
        return tournament

#    def add_players_to_tournament(self, player_list):
#        t_players = self.db.table('tournaments').__getitem__[-1][]
#        for player in player_list:
#            serialized_player = self.player.serialize_player(player)

    def serialize_tournament(self, tournament):
        serialized_tournament = {'Nom': tournament.name,
                                 'Classement': tournament.player_ratings,
                                 'Nombre de rondes': tournament.rounds_nr,
                                 'Rondes': tournament.rounds
                                 }
        return serialized_tournament

    def deserialize_tournament(self, tournament):
        name = tournament[0]['Nom']
        player_ratings = tournament[0]['Classement']
        rounds_nr = tournament[0]['Nombre de rondes']
        rounds = tournament[0]['Rondes']
        deserialized_tournament = Tournament(name, player_ratings, rounds_nr, rounds)
        return deserialized_tournament

    def deserialize_player_ratings(self, active_tournament):
        player_ratings = list()
        for rated_player in active_tournament.player_ratings:
            rated_player = (self.player.deserialize_player(rated_player[0]), rated_player[1])
            player_ratings.append(rated_player)
        return player_ratings

    def sort_players(self, players):
        players.sort(reverse=True, key=lambda x: (x[1], x[0].elo))
        return players

    @staticmethod
    def save_tournament(serialized_tournament, db):
        tournaments_table = db.table('tournaments')
        tournaments_table.insert(serialized_tournament)

    def erase_tournament(self, active_tournament, db):
        q = Query()
        name = active_tournament['Nom']
        db.table('tournaments').remove(q.Nom == name)
        print('Tournoi effacé')

    def get_tournament(self, name, db):
        q = Query()
        tournoi = db.table('tournaments').search(q.Nom == name)
        return tournoi

    def get_created_tournament(self, db):
        name = db.table('tournaments').all()[-1]['Nom']
        rounds_nr = db.table('tournaments').all()[-1]['Nombre de rondes']
        q = Query()
        rounds = db.table('tournaments').all()[-1]['Rondes']
        player_ratings = db.table('tournaments').all()[-1]['Classement']

        created_tournament = Tournament(name, player_ratings, rounds_nr, rounds)
        print(created_tournament.name, created_tournament.player_ratings, created_tournament.rounds_nr,
              created_tournament.rounds)
        return created_tournament


class Round:
    def __init__(self, name, matches):
        self.name = name
        self.matches = matches

    def create_round1_matches(self, player_ratings):
        r1_players = list()
        for i in range(0, int(len(player_ratings) / 2)):
            j = i + len(player_ratings) / 2
            r1_players.append(player_ratings[i])
            r1_players.append(player_ratings[int(j)])

        player_ratings.clear()
        for player in r1_players:
            player_ratings.append(player)
        return player_ratings

#    def add_scores_for_round_list(players):
#        r_players = list()
#        for i in range(0, len(players)):
#            r_player = Player(name=players[i].name, elo=players[i].elo, score=round_scores[i])
#            r_players.append(r_player)

#        return r_players


class Match:

    def __init__(self, player_white, player_black, score_white, score_black):
        self.player_white = (player_white, score_white)
        self.player_black = (player_black, score_black)
        self.match = (self.player_white, self.player_black)


class Test:
    def __init__(self):
        self.player = Player(str(), int())
        self.db = TinyDB('db.json')

    def test_created_tournament(self, tournament, created_tournament):
        expected_tournament = tournament

        if expected_tournament.name == created_tournament.name \
                and expected_tournament.rounds_nr == created_tournament.rounds_nr \
                and expected_tournament.rounds == created_tournament.rounds \
                and expected_tournament.players == created_tournament.players:
            print('La saisie et l\'entree de la base de donnees concordent!')
            return True
        else:
            self.db.table('tournaments').remove(doc_ids=[len(self.db.table('tournaments'))])
            print('Effacement du dernier tournoi cree effectue')

    def test_created_player(self, player, created_player):
        expected_player = player

        if expected_player.name == created_player.name and expected_player.elo == created_player.elo:
            print('La saisie et l\'entree de la base de donnees concordent!')
            return True
        else:
            self.db.table('players').remove(doc_ids=[len(self.db.table('players'))])
            print('Effacement du dernier joueur cree effectue')


class Serializer:

    def serialize_tournament(self, tournament):
        pass

    def serialize_round(self, round):
        serialized_round = [{'name': round.name, 'matches': self.serialize_matches(round.matches)}]
        return serialized_round

    def serialize_matches(self, matches):
        serialized_matches = list()
        for match in matches:
            serialized_player_white = self.serialize_player(match.match[0][0])
            serialized_player_black = self.serialize_player(match.match[1][0])
            serialized_match = ((serialized_player_white, match.match[0][1]), (serialized_player_black, match.match[1][1]))
            serialized_matches.append(serialized_match)
        return serialized_matches

    def serialize_player(self, player):
        serialized_player = {'Nom': player.name, 'ELO': player.elo}
        return serialized_player

