from tinydb import TinyDB, Query
import datetime

# Preliminary variable initializations.
db = TinyDB('db.json')
players_table = db.table('players')
tournaments_table = db.table('tournaments')


class View:
    def __init__(self):
        self.db = db

    @staticmethod
    def display_main_menu():
        """Displays main menu."""
        main_menu = dict()
        main_menu['1'] = 'Menu création'
        main_menu['2'] = 'Menu rapports'
        main_menu['3'] = 'Quitter le programme'

        options = main_menu.keys()
        print('***********************************************\nMENU PRINCIPAL:')
        for entry in options:
            print(entry, main_menu[entry])

        selection = input('***********************************************\nChoisissez une option: ')
        return selection

    @staticmethod
    def display_creation_menu():
        """Displays creation menu."""
        creation_menu = dict()
        creation_menu['1'] = 'Créer un nouveau tournoi'
        creation_menu['2'] = 'Créer/Modifier un joueur'
        creation_menu['3'] = 'Importer les joueurs du tournoi'
        creation_menu['4'] = 'Créer une nouvelle ronde'
        creation_menu['5'] = 'Menu principal'

        options = creation_menu.keys()
        print('***********************************************\nMENU TOURNOI:')
        for entry in options:
            print(entry, creation_menu[entry])

        selection = input('***********************************************\nChoisissez une option: ')
        return selection

    @staticmethod
    def display_player_submenu():
        """Displays player submenu."""
        player_submenu = dict()
        player_submenu['1'] = 'Créer un nouveau joueur'
        player_submenu['2'] = 'Supprimer un joueur existant'
        player_submenu['3'] = 'Menu création'

        options = player_submenu.keys()
        print('***********************************************\nMENU TOURNOI:')
        for entry in options:
            print(entry, player_submenu[entry])

        selection = input('***********************************************\nChoisissez une option: ')
        return selection

    @staticmethod
    def display_reports_menu():
        """Displays reports menu."""
        reports_menu = dict()
        reports_menu['1'] = 'Liste de tous les acteurs'
        reports_menu['2'] = 'Liste de tous les joueurs d\'un tournoi'
        reports_menu['3'] = 'Liste de tous les tournois'
        reports_menu['4'] = 'Liste de toutes les rondes d\'un tournoi'
        reports_menu['5'] = 'Liste de tous les matchs d\'un tournoi'
        reports_menu['6'] = 'Menu principal'

        options = reports_menu.keys()
        print('\n***********************************************\nMENU RECHERCHE:')
        for entry in options:
            print(entry, reports_menu[entry])
        selection = input('***********************************************\nChoisissez une option: ')
        return selection

    @staticmethod
    def display_menu_options(length):
        """Indicates how many choices user has in active menu."""
        print('\n***********************************************\nVeuillez choisir une option entre 1 et', str(length))

    @staticmethod
    def display_player_ratings(player_ratings):
        """Displays current player ratings in tournament."""
        print('\nCLASSEMENT DES PARTICIPANTS:\n Nom  ELO  Score')
        for i in range(0, len(player_ratings)):
            print(players_table.get(doc_id=player_ratings[i][0])['Nom'],
                  players_table.get(doc_id=player_ratings[i][0])['ELO'],
                  player_ratings[i][1])

    @staticmethod
    def display_round_matches(player_ratings):
        """Displays current round matches to be played."""
        print('\nMATCHES DE LA RONDE: ')
        for i in range(0, len(player_ratings), 2):
            print(players_table.get(doc_id=player_ratings[i][0])['Nom'], "(BLANCS)",
                  "contre",
                  players_table.get(doc_id=player_ratings[i+1][0])['Nom'], "(NOIRS)")

    @staticmethod
    def display_current_match(i, player_ratings):
        """Displays player name and colour for current match."""
        print('MATCH', int(i/2+1))
        print(players_table.get(doc_id=player_ratings[i][0])['Nom'], "(BLANCS)",
              "contre",
              players_table.get(doc_id=player_ratings[i+1][0])['Nom'], "(NOIRS)")

    def display_actor_list(self):
        """Displays all players registered in database sorted by name, or by ELO."""
        actor_list = list()
        for actor in players_table:
            actor_list.append(actor)
        user_choice = self.input_user_choice_sorting()
        print("Liste de tous les acteurs: ")
        if user_choice == '1':
            actor_list.sort(key=lambda x: x['Nom'])
            for player in actor_list:
                print(player)
        elif user_choice == '2':
            actor_list.sort(reverse=True, key=lambda x: x['ELO'])
            for player in actor_list:
                print(player)

    def display_tournament_player_list(self):
        """Displays all tournament players registered in database sorted by name, or by ELO."""
        tournament_name = self.input_name("nom du tournoi")
        tournament = tournaments_table.get(Query().Nom == tournament_name)
        player_list = list()
        for rated_player in tournament['Classement']:
            player_list.append(players_table.get(doc_id=rated_player[0]))
        user_choice = self.input_user_choice_sorting()
        print("Liste de tous les joueurs du tournoi de", tournament_name, ": ")
        if user_choice == '1':
            player_list.sort(key=lambda x: x['Nom'])
            for player in player_list:
                print(player)
        elif user_choice == '2':
            player_list.sort(reverse=True, key=lambda x: x['ELO'])
            for player in player_list:
                print(player)

    @staticmethod
    def display_tournament_list():
        """Displays the list of all tournament names."""
        for tournament in tournaments_table:
            print(tournament['Nom'])

    def display_all_tournament_rounds(self):
        """Displays all rounds for a given tournament."""
        tournament_name = self.input_name("nom du tournoi")
        tournament = tournaments_table.get(Query().Nom == tournament_name)
        print("Rondes du tournoi de", tournament_name, ": ")
        for current_round in tournament['Rondes']:
            print(current_round)

    def display_all_round_matches(self):
        """Displays the list of already played matches for a given tournament."""
        tournament_name = self.input_name("nom du tournoi")
        tournament = tournaments_table.get(Query().Nom == tournament_name)
        print("Matches du tournoi de", tournament_name, "ayant eu lieu: ")
        for match in tournament['Matches joues']:
            print(players_table.get(doc_id=match[0])['Nom'], "(BLANCS) contre",
                  players_table.get(doc_id=match[1])['Nom'], "(NOIRS)")

    @staticmethod
    def search_player_by_name(players_table, name):
        """Displays a player stored in all-players database."""
        result = players_table.search(Query().Nom == name)
        print(result)

    @staticmethod
    def search_tournament_by_name(tournaments_table, name):
        """Displays a tournament name stored in the tournaments database."""
        result = tournaments_table.search(Query().Nom == name)
        print(result)

    @staticmethod
    def display_imported_players(players_id_list):
        """Displays the list of imported players in current tournament."""
        for player_id in players_id_list:
            print(players_table.get(doc_id=player_id))

    @staticmethod
    def display_players_list_length(players_list):
        """Displays the number of imported players in current tournament."""
        print('Nombre de joueurs importés: ', len(players_list))

    def input_name(self, attr_name):
        """Input method for tournament or player name."""
        accepted_letters_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
                                 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '-']
        try:
            tested_input = input("Entrez le " + attr_name + ": ")
            i = 0
            while i < len(tested_input):
                if tested_input[i].lower() not in accepted_letters_list:
                    raise ValueError
                else:
                    i += 1
            return tested_input
        except ValueError:
            print("N'accepte que des lettres (caractères non spéciaux) et le tiret '-'")
            return self.input_name(attr_name)

    def input_tour_rounds_nr(self):
        """Input method for tournament number of rounds (default: 4)."""
        try:
            t_rounds_nr = input('Veuillez entrer le nombre de rondes du tournoi (par défaut: "4"): ')
            if len(t_rounds_nr) == 0:
                t_rounds_nr = 4
                return t_rounds_nr
            else:
                if int(t_rounds_nr) < 1:
                    raise ValueError
                return int(t_rounds_nr)
        except ValueError:
            print("Vous devez entrer un nombre! (entier supérieur à zéro)")
            return self.input_tour_rounds_nr()

    def input_date(self, date_attr):
        """Input method for tournament date and player date of birth, that checks if input date exists."""
        try:
            date = input("Entrez la " + date_attr + "(JJ/MM/AAAA): ")
            datetime.datetime.strptime(date, '%d/%m/%Y')
            return date
        except ValueError:
            print("Erreur de saisie de la date (format JJ/MM/AAAA)")
            return self.input_date(date_attr)

    def input_time_ctrl(self):
        """Input method for tournament time control."""
        time_ctrl_list = ["bullet", "blitz", "coup rapide"]
        time_ctrl = input("Entrez la cadence de jeu du tournoi (bullet, blitz ou coup rapide): ")
        try:
            if time_ctrl.lower() in time_ctrl_list:
                return time_ctrl.lower()
        except ValueError:
            print("Veuillez entrer 'bullet', 'blitz' ou 'coup rapide'")
            return self.input_time_ctrl()

    @staticmethod
    def input_desc():
        """Input method for tournament description."""
        desc = input("Entrez ici les remarques générales du directeur du tournoi: ")
        return desc

    def input_player_sex(self):
        """Input method for player sex."""
        sex_list = ['m', 'f', 'a']
        try:
            sex = input("Entrez le sexe du joueur ('M' pour masculin, 'F' pour féminin, 'A' pour autre): ")
            if sex.lower() in sex_list:
                return sex.capitalize()
            else:
                raise ValueError
        except ValueError:
            print("Veuillez entrer 'M' pour masculin, 'F' pour féminin, 'A' pour autre")
            return self.input_player_sex()

    def input_player_elo(self):
        """Input method for player ELO that checks if ELO exists."""
        try:
            elo = input('Entrez le classement ELO du joueur: ')
            if int(elo):
                try:
                    if int(elo) < 1000 or int(elo) > 2900:
                        raise ValueError
                    else:
                        return int(elo)
                except ValueError:
                    print("Le classement ELO doit être un entier compris entre 1000 et 2900!")
                    return self.input_player_elo()
            else:
                raise ValueError
        except ValueError:
            print("Vous devez entrer un nombre! (entier supérieur compris entre 1000 et 2900)")
            return self.input_player_elo()

    def input_player_scores_checked(self):
        """Checks if the sum of players scores is equal to 1."""
        score_white = self.input_player_score_white()
        score_black = self.input_player_score_black()
        try:
            if score_white + score_black == 1:
                return score_white, score_black
            else:
                raise ValueError
        except ValueError:
            print("La somme des scores des deux joueurs doit être égale à 1!")
            return self.input_player_scores_checked()

    def input_player_score_white(self):
        """Input method for white player's score."""
        accepted_scores = ['0', '0.5', '1']
        try:
            score_w = input("Entrez le score du joueur BLANCS ('0', '0.5' ou '1'): ")
            if score_w in accepted_scores:
                return float(score_w)
            raise ValueError
        except ValueError:
            print("Le résultat du joueur doit être 0, 0.5 ou 1!")
            return self.input_player_score_white()

    def input_player_score_black(self):
        """Input method for black player's score."""
        accepted_scores = ['0', '0.5', '1']
        try:
            score_b = input("Entrez le score du joueur NOIRS ('0', '0.5' ou '1'): ")
            if score_b in accepted_scores:
                return float(score_b)
            else:
                raise ValueError
        except ValueError:
            print("Le résultat du joueur doit être 0, 0.5 ou 1!")
            return self.input_player_score_black()

    def input_user_choice_addition(self):
        """Checks if user confirms addition."""
        try:
            user_choice = input("Confirmer l'ajout? Y/N: ")
            if user_choice.lower() == 'y' or user_choice.lower() == 'n':
                return user_choice
            else:
                raise ValueError
        except ValueError:
            print("Veuillez choisir Y/N")
            return self.input_user_choice_addition()

    def input_user_choice_deletion(self):
        """Checks if user confirms deletion."""
        try:
            user_choice = input("Confirmer la suppression? Y/N: ")
            if user_choice.lower() == 'y' or user_choice.lower() == 'n':
                return user_choice.lower()

        except ValueError:
            print("Veuillez choisir Y/N")
            return self.input_user_choice_deletion()

    def input_user_choice_import(self):
        """Checks if user confirms import."""
        try:
            user_choice = input("Continuer l'importation? Y/N: ")
            if user_choice.lower() == 'y' or user_choice.lower() == 'n':
                return user_choice

        except ValueError:
            print("Veuillez choisir Y/N")
            return self.input_user_choice_import()

    def input_user_choice_sorting(self):
        """Checks what kind of sorting user wants."""
        try:
            user_choice = input("Classer par\n    Ordre alphabétique (entrez '1')\n    Classement ELO (entrez '2')\n")
            if user_choice == '1' or user_choice == '2':
                return user_choice
            else:
                raise ValueError
        except ValueError:
            print("Veuillez choisir 1 ou 2")
            return self.input_user_choice_sorting()
