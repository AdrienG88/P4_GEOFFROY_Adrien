from tinydb import TinyDB, Query
import random


class Player:
    def __init__(self, name, first_name, birthdate, sex, elo):
        self.name = name
        self.first_name = first_name
        self.birthdate = birthdate
        self.sex = sex
        self.elo = elo
        self.db = TinyDB('db.json')

    @staticmethod
    def get_created_player(db):
        """Gets all data from the last created player stored in database.

        Attrs:
        - db (json): database from TinyDB.

        Returns:
        - the last stored player data turned into a Player-class instance.
        """
        name = db.table('players').all()[-1]['Nom']
        first_name = db.table('players').all()[-1]['Prenom']
        birthdate = db.table('players').all()[-1]['Date de naissance']
        sex = db.table('players').all()[-1]['Sexe']
        elo = db.table('players').all()[-1]['ELO']
        created_player = Player(name, first_name, birthdate, sex, elo)
        return created_player

    def save_player(self, serialized_player):
        """Saves player data in database.

        Attrs:
        - serialized_player (dict): the serialized version of a Player-class instance.

        Returns:
        - the same serialized_player variable.
        """
        players_table = self.db.table('players')
        players_table.insert(serialized_player)
        return serialized_player


class Tournament:
    def __init__(self, name, place, date, player_ratings, rounds_nr, rounds, time_ctrl, desc, matchmaking_data):
        self.name = name
        self.place = place
        self.date = date
        self.player_ratings = player_ratings
        self.rounds_nr = rounds_nr
        self.rounds = rounds
        self.time_ctrl = time_ctrl
        self.desc = desc
        self.matchmaking_data = matchmaking_data
        self.db = TinyDB('db.json')
        self.player = Player(str(), str(), str(), str(), int())

    @staticmethod
    def create_tournament_instance(name, place, date, rounds_nr, time_ctrl, desc):
        """Creates a Tournament-class instance from user input data.

        Attrs:
        - name (str): user-input tournament name.
        - place (str): user-input tournament place.
        - data (str): user-input tournament date.
        - rounds_nr (int): user-input tournament number of rounds (default=4).
        - time-ctrl (str): user-input time control tournament parameter.
        - desc (str): user-input tournament general description and/or comments.

        Returns:
        - a Tournament-class instance.
        """
        player_ratings = list()
        rounds = list()
        matchmaking_data = list()
        tournament =\
            Tournament(name, place, date, player_ratings, rounds_nr, rounds, time_ctrl, desc, matchmaking_data)
        return tournament

    @staticmethod
    def get_created_tournament(db):
        """Gets all data from the last created tournament stored in database.

        Attrs:
        - db (json): database from TinyDB.

        Returns:
        - the last stored tournament data turned into a Tournament-class instance.
        """
        name = db.table('tournaments').all()[-1]['Nom']
        place = db.table('tournaments').all()[-1]['Lieu']
        date = db.table('tournaments').all()[-1]['Date']
        player_ratings = db.table('tournaments').all()[-1]['Classement']
        rounds_nr = db.table('tournaments').all()[-1]['Nombre de rondes']
        rounds = db.table('tournaments').all()[-1]['Rondes']
        time_ctrl = db.table('tournaments').all()[-1]['Cadence']
        desc = db.table('tournaments').all()[-1]['Description']
        matchmaking_data = db.table('tournaments').all()[-1]['Matches joues']
        created_tournament =\
            Tournament(name, place, date, player_ratings, rounds_nr, rounds, time_ctrl, desc, matchmaking_data)

        return created_tournament

    @staticmethod
    def get_saved_tournament(name, db):
        """Searches a named tournament in the database.

        Attrs:
        - name (str): the name of the searched tournament.
        - db (json): database from TinyDB.

        Returns:
        - the queried tournament from database.
        """
        q = Query()
        tournament = db.table('tournaments').search(q.Nom == name)
        return tournament

    @staticmethod
    def save_tournament(serialized_tournament, db):
        """Replaces and saves tournament data in database.

        Attrs:
        - serialized_tournament (dict): the serialized version of a Tournament-class instance.

        Returns:
        - the same serialized_tournament variable.
        """
        q = Query()
        name = serialized_tournament['Nom']
        db.table('tournaments').remove(q.Nom == name)

        tournaments_table = db.table('tournaments')
        tournaments_table.insert(serialized_tournament)
        message = 3
        return message

    @staticmethod
    def sort_players(player_ratings, players_table):
        """Sorts players by by alphabetical name, score, then ELO.

        Attrs:
        - player_ratings (list): the list of (player id, score) tuples.
        - players_table (json): a JSON table containing all created players.

        Returns:
        - the sorted list of (player id, score) tuples.
        """
        tmp_player_ratings = list()
        for player in player_ratings:
            tmp_rated_player = players_table.get(doc_id=player[0]), player[1]
            tmp_player_ratings.append(tmp_rated_player)
        tmp_player_ratings.sort(key=lambda x: x[0]['Nom'])
        tmp_player_ratings.sort(reverse=True, key=lambda x: (x[1], x[0]['ELO']))
        player_ratings.clear()
        for tmp_player in tmp_player_ratings:
            rated_player = [players_table.get(Query().Nom == tmp_player[0]['Nom']).doc_id, tmp_player[1]]
            player_ratings.append(rated_player)
        return player_ratings


class Round:
    def __init__(self, name, matches):
        self.name = name
        self.matches = matches

    @staticmethod
    def pair_round1_matches(player_ratings):
        """Changes players order to pair players for the first round of the tournament.

        Attrs:
        - player_ratings (list): the list of (player id, score) tuples.

        Returns:
        - a sorted players list in order to pair them for the first round of the tournament.
        """
        coin_flip_player_ratings = list()
        for i in range(0, int(len(player_ratings) / 2)):
            j = i + len(player_ratings) / 2
            coin_flip = random.randint(0, 1)
            if coin_flip == 0:
                coin_flip_player_ratings.append(player_ratings[i])
                coin_flip_player_ratings.append(player_ratings[int(j)])
            else:
                coin_flip_player_ratings.append(player_ratings[int(j)])
                coin_flip_player_ratings.append(player_ratings[i])

        player_ratings.clear()
        for player in coin_flip_player_ratings:
            player_ratings.append(player)
        return player_ratings

    def pair_other_rounds_matches(self, player_ratings, matchmaking_data):
        """Changes players order to pair players for any round of the tournament (except the first one).

        Attrs:
        - player_ratings (list): the list of (player id, score) tuples.

        Returns:
        - a sorted players list in order to pair them for any round of the tournament (except the first one).
        """
        i = 1
        tested_player_ratings = list()
        while len(player_ratings) > 2:
            self.matchmaking_data_test(i, player_ratings, tested_player_ratings, matchmaking_data)
        tested_player_ratings.append(player_ratings[0])
        tested_player_ratings.append(player_ratings[1])

        coin_flip_player_ratings = list()
        for i in range(0, len(tested_player_ratings), 2):
            coin_flip = random.randint(0, 1)
            if coin_flip == 0:
                coin_flip_player_ratings.append(tested_player_ratings[i])
                coin_flip_player_ratings.append(tested_player_ratings[i+1])
            else:
                coin_flip_player_ratings.append(tested_player_ratings[i+1])
                coin_flip_player_ratings.append(tested_player_ratings[i])

        player_ratings.clear()
        for player in coin_flip_player_ratings:
            player_ratings.append(player)
        return player_ratings

    def matchmaking_data_test(self, i, player_ratings, tested_player_ratings, matchmaking_data):
        """Tests if a match already took place not to pair players that already played against each other.

        Attrs:
        - i (int): the index value for the second player in the tested match.
        - player_ratings (list): the list of (player id, score) tuples.
        - tested_player_ratings (list) : the list of (player id, score) tuples once tested (used for pairing).
        - matchmaking_data (list) : the list of already played matches (list of (player id, player id) tuples).

        Returns:
        - a tested list of players used for pairing players.
        """
        if (player_ratings[0][0], player_ratings[i][0]) not in matchmaking_data and\
                (player_ratings[i][0], player_ratings[0][0]) not in matchmaking_data:
            tested_player_ratings.append(player_ratings[0])
            tested_player_ratings.append(player_ratings[i])
            del player_ratings[0]
            del player_ratings[i-1]
            return tested_player_ratings
        else:
            i += 1
            self.matchmaking_data_test(i, player_ratings, tested_player_ratings, matchmaking_data)


class Match:

    def __init__(self, player_white, player_black, score_white, score_black):
        self.player_white = (player_white, score_white)
        self.player_black = (player_black, score_black)
        self.match = (self.player_white, self.player_black)


class Test:
    def __init__(self):
        self.player = Player(str(), str(), str(), str(), int())
        self.db = TinyDB('db.json')

    def test_created_player(self, player, created_player):
        """Tests if user-input player matches with saved player in database. Deletes it otherwise.

        Attrs:
        - player (Player): the active Player-class instance.
        - created_player (Player): a Player-class instance created from downloaded entry in database.

        Returns:
        - test_message value to be displayed by View. Deletes saved player if mismatch.
        """
        expected_player = player

        if expected_player.name == created_player.name and expected_player.elo == created_player.elo:
            test_message = 4
            return test_message
        else:
            self.db.table('players').remove(doc_ids=[len(self.db.table('players'))])
            test_message = 2
            return test_message

    def test_created_tournament(self, tournament, created_tournament):
        """Tests if user-input tournament matches with saved tournament in database. Deletes it otherwise.

        Attrs:
        - tournament (Tournament): the active Tournament-class instance.
        - created_tournament (Tournament): a Tournament-class instance created from downloaded entry in database.

        Returns:
        - test_message value to be displayed by View. Deletes saved tournament if mismatch.
        """
        expected_tournament = tournament

        if expected_tournament.name == created_tournament.name \
                and expected_tournament.rounds_nr == created_tournament.rounds_nr:
            test_message = 4
            return test_message
        else:
            self.db.table('tournaments').remove(doc_ids=[len(self.db.table('tournaments'))])
            test_message = 1
            return test_message


class Deserializer:

    def deserialize_tournament(self, tournament):
        """Turns a serialized tournament into a Tournament-class instance.

        Attrs:
        - tournament (dict): a serialized tournament from database.

        Returns:
        - a Tournament-class instance created from a serialized tournament.
        """
        name = tournament[0]['Nom']
        place = tournament[0]['Lieu']
        date = tournament[0]['Date']
        player_ratings = self.deserialize_player_ratings(tournament[0]['Classement'])
        rounds_nr = int(tournament[0]['Nombre de rondes'])
        rounds = self.deserialize_rounds(tournament[0]['Rondes'])
        time_ctrl = tournament[0]['Cadence']
        desc = tournament[0]['Description']
        matchmaking_data = self.deserialize_matchmaking_data(tournament[0]['Matches joues'])
        deserialized_tournament =\
            Tournament(name, place, date, player_ratings, rounds_nr, rounds, time_ctrl, desc, matchmaking_data)
        return deserialized_tournament

    @staticmethod
    def deserialize_player_ratings(player_ratings):
        """Turns a list of (str, str) tuples from database into a list of (int, float) tuples.

        Attrs:
        - player_ratings (list): a list of (str, str) tuples.

        Returns:
        - a list of (int, float) tuples.
        """
        deserialized_player_ratings = list()
        for rated_player in player_ratings:
            deserialized_rated_player = [rated_player[0], float(rated_player[1])]
            deserialized_player_ratings.append(deserialized_rated_player)
        return deserialized_player_ratings

    def deserialize_rounds(self, rounds):
        """Turns a list of serialized rounds into a list of Round-class instances.

        Attrs:
        - rounds (list): a list of serialized rounds.

        Returns:
        - a list of Round-class instances."""
        deserialized_rounds = list()
        for current_round in rounds:
            name = current_round['Nom']
            matches = self.deserialize_matches(current_round['Matches'])
            deserialized_round = Round(name, matches)
            deserialized_rounds.append(deserialized_round)
        return deserialized_rounds

    def deserialize_matches(self, matches):
        """Turns a list of serialized matches into a list of Match-class instances.

        Attrs:
        - matches (list): a list of serialized matches.

        Returns:
        - a list of Match-class instances."""
        deserialized_matches = list()
        for match in matches:
            player_white = self.deserialize_player(match[0][0])
            player_black = self.deserialize_player(match[1][0])
            score_white = float(match[0][1])
            score_black = float(match[1][1])
            deserialized_match = Match(player_white, player_black, score_white, score_black)
            deserialized_matches.append(deserialized_match)
        return deserialized_matches

    @staticmethod
    def deserialize_matchmaking_data(matchmaking_data):
        """Turns a serialized list of [player id, player id] lists into a list of (player id, player id) tuples.

        Attrs:
        - matchmaking_data (list): a list of [player id, player id] lists.

        Returns:
        - a list of (player id, player id) tuples.
        """
        deserialized_matchmaking_data = list()
        for match in matchmaking_data:
            deserialized_match = match[0], match[1]
            deserialized_matchmaking_data.append(deserialized_match)
        return deserialized_matchmaking_data

    @staticmethod
    def deserialize_player(player):
        """Turns a serialized player into a Player-class instance.

        Attrs:
        - player (dict): a serialized player from database.

        Returns:
        - a Player-class instance created from a serialized player."""
        name = player['Nom']
        first_name = player['Prenom']
        birthdate = player['Date de naissance']
        sex = player['Sexe']
        elo = player['ELO']

        deserialized_player = Player(name, first_name, birthdate, sex, elo)
        return deserialized_player


class Serializer:

    def serialize_tournament(self, tournament):
        """Turns a Tournament-class instance into a serialized object.

        Attrs:
        - tournament (Tournament): a Tournament-class instance.

        Returns:
        - a dictionary containing the Tournament-class instance information."""
        serialized_tournament = {'Nom': tournament.name,
                                 'Lieu': tournament.place,
                                 'Date': tournament.date,
                                 'Classement': self.serialize_player_ratings(tournament.player_ratings),
                                 'Nombre de rondes': tournament.rounds_nr,
                                 'Rondes': self.serialize_rounds(tournament.rounds),
                                 'Cadence': tournament.time_ctrl,
                                 'Description': tournament.desc,
                                 'Matches joues': self.serialize_matchmaking_data(tournament.matchmaking_data)}
        return serialized_tournament

    @staticmethod
    def serialize_player_ratings(player_ratings):
        """Turns a list of tuples into a list of lists.

        Attrs:
        - player_ratings (list): a list of (player id, score) tuples.

        Returns:
        - a list of lists containing the original list information."""
        serialized_player_ratings = list()
        for rated_player in player_ratings:
            serialized_rated_player = [rated_player[0], float(rated_player[1])]
            serialized_player_ratings.append(serialized_rated_player)
        return serialized_player_ratings

    def serialize_rounds(self, rounds):
        """Turns a Round-class instances list into a serialized object.

        Attrs:
        - rounds (list): a list of Round-class instances.

        Returns:
        - a dictionary containing the rounds list information."""
        serialized_rounds = list()
        for current_round in rounds:
            serialized_round = {'Nom': current_round.name, 'Matches': self.serialize_matches(current_round.matches)}
            serialized_rounds.append(serialized_round)
        return serialized_rounds

    def serialize_matches(self, matches):
        """Turns a Match-class instances list into a serialized object.

        Attrs:
        - matches (list): a list of Match-class instances.

        Returns:
        - a list containing the matches list information."""
        serialized_matches = list()
        for match in matches:
            serialized_player_white = self.serialize_player(match.match[0][0])
            serialized_player_black = self.serialize_player(match.match[1][0])
            serialized_match = ((serialized_player_white, match.match[0][1]),
                                (serialized_player_black, match.match[1][1]))
            serialized_matches.append(serialized_match)
        return serialized_matches

    @staticmethod
    def serialize_matchmaking_data(matchmaking_data):
        """Turns a list of tuples into a list of lists.

        Attrs:
        - matchmaking_data (list): a list of tuples.

        Returns:
        - a list of lists containing matchmaking_data information.
        """
        serialized_matchmaking_data = list()
        for match in matchmaking_data:
            serialized_match = (match[0], match[1])
            serialized_matchmaking_data.append(serialized_match)
        return serialized_matchmaking_data

    @staticmethod
    def serialize_player(player):
        """Turns a Player-class instance into a serialized object.

        Attrs:
        - player (Player): a Player-class instance.

        Returns:
        - a dictionary containing the Player-class instance information."""
        serialized_player = {'Nom': player.name,
                             'Prenom': player.first_name,
                             'Date de naissance': player.birthdate,
                             'Sexe': player.sex,
                             'ELO': player.elo}
        return serialized_player
