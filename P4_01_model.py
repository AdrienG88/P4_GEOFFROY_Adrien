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

#a revoir
#    def create_player_instances(players):
#        for i in range(0, len(serialized_players)):
#            player = Player(serialized_players[i]['nom'],
#                            serialized_players[i]['elo'],
#                            serialized_players[i]['score']
#                            )
#            players.append(player)
#            print(player.name, player.elo, player.score)

    def serialize_player(self, player):
        serialized_player = {'Nom': player.name, 'ELO': player.elo}
        return serialized_player

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
    def __init__(self, name, rounds_nr, rounds, players):
        self.name = name
        self.rounds_nr = rounds_nr
        self.rounds = rounds
        self.players = players
        self.db = TinyDB('db.json')

    def create_tournament(self, name, rounds_nr):
        rounds = list()
        players = list()
        tournament = Tournament(name, rounds_nr, rounds, players)
        return tournament


    def serialize_tournament(self, tournament):
        serialized_tournament = {'Nom': tournament.name,
                                 'Nombre de rondes': tournament.rounds_nr,
                                 'Rondes': tournament.rounds,
                                 'Joueurs': tournament.players
                                 }
        return serialized_tournament

    def save_tournament(self, serialized_tournament):
        tournaments_table = self.db.table('tournaments')
        tournaments_table.insert(serialized_tournament)

    def get_created_tournament(self, db):
        name = db.table('tournaments').all()[-1]['Nom']
        rounds_nr = db.table('tournaments').all()[-1]['Nombre de rondes']
        rounds = list()
        for elt in db.table('tournaments').all[-1].Rondes:
            rounds.append(elt)
        players = list()
        for elt in db.table('tournaments').all[-1].Joueurs:
            players.append(elt)

        created_tournament = Tournament(name, rounds_nr, rounds, players)
        print(created_tournament.name, created_tournament.rounds_nr)
        return created_tournament

    def to_json(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__))


class Round:
    def __init__(self, name, matches):
        self.name = name
        self.matches = matches

#    def add_scores_for_round_list(players):
#        r_players = list()
#        for i in range(0, len(players)):
#            r_player = Player(name=players[i].name, elo=players[i].elo, score=round_scores[i])
#            r_players.append(r_player)

#        return r_players


class Test:
    def __init__(self):
        self.player = Player(str(), int())
        self.db = TinyDB('db.json')

    def test_created_tournament(self, tournament, created_tournament):
        expected_tournament = tournament

        if expected_tournament.name == created_tournament.name \
                and expected_tournament.rounds_nr == created_tournament.rounds_nr:
            print('La saisie et l\'entree de la base de donnees concordent!')
            return True
        else:
            self.db.table('tournaments').remove(doc_ids=[len(self.db.table('tournaments'))])
            print('Entree effacee')

    def test_created_player(self, player, created_player):
        expected_player = player

        if expected_player.name == created_player.name and expected_player.elo == created_player.elo:
            print('La saisie et l\'entree de la base de donnees concordent!')
            return True
        else:
            self.db.table('players').remove(doc_ids=[len(self.db.table('players'))])
            print('Entree effacee')
