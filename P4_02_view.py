from tinydb import TinyDB, Query
db = TinyDB('db.json')
players_table = db.table('players')
tournaments_table = db.table('tournaments')


class View:
    def __init__(self):
        self.db = db

    # FONCTIONS D'AFFICHAGE DES MENUS

    @staticmethod
    def display_main_menu():
        # defines all options available in main menu
        main_menu = dict()
        main_menu['1'] = 'Menu création'
        main_menu['2'] = 'Menu recherche'
        main_menu['3'] = 'Menu rapports'
        main_menu['4'] = 'Quitter le programme'

        options = main_menu.keys()
        print('***********************************************\nMENU PRINCIPAL:')
        for entry in options:
            print(entry, main_menu[entry])

        selection = input('***********************************************\nChoisissez une option: ')
        return selection

    @staticmethod
    def display_creation_menu():
        # defines all options available in creation menu
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
    def display_search_menu():
        search_menu = dict()
        search_menu['1'] = 'Rechercher un joueur'
        search_menu['2'] = 'Rechercher un tournoi'
        search_menu['3'] = 'Menu principal'

        options = search_menu.keys()
        print('\n***********************************************\nMENU RECHERCHE:')
        for entry in options:
            print(entry, search_menu[entry])
        selection = input('***********************************************\nChoisissez une option: ')
        return selection

    @staticmethod
    def display_reports_menu():
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

    # NOMBRE DE CHOIX DU MENU
    @staticmethod
    def display_menu_options(length):
        print('\n***********************************************\nVeuillez choisir une option entre 1 et', str(length))

    # METHODES D'AFFICHAGE DES RONDES

    @staticmethod
    def display_player_ratings(player_ratings):
        print('CLASSEMENT DES PARTICIPANTS:\n Nom  ELO  score')
        for i in range(0, len(player_ratings)):
            print(player_ratings[i][0].name, player_ratings[i][0].elo, player_ratings[i][1])

    @staticmethod
    def display_round_matches(player_ratings):
        print('\nMATCHES DE LA RONDE: ')
        for i in range(0, len(player_ratings), 2):
            print(player_ratings[i][0].name, "contre", player_ratings[i + 1][0].name)

    @staticmethod
    def input_round_matches(i, player_ratings):
            print('MATCH', int(i/2+1))
            print(player_ratings[i][0].name, "contre", player_ratings[i + 1][0].name)

    # METHODES D'AFFICHAGE DES DONNEES DE LA BASE DE DONNEES

    @staticmethod
    def display_tournament_list():
        for tournament in tournaments_table:
            print(tournament)

    @staticmethod
    def display_player_list():
        for player in players_table:
            print(player)

    @staticmethod
    def search_player_by_name(players_table, name):
        joueur = Query()
        result = players_table.search(joueur.Nom == name)
        print(result)

    @staticmethod
    def search_tournament_by_name(tournaments_table, name):
        tour = Query()
        result = tournaments_table.search(tour.Nom == name)
        print(result)

    @staticmethod
    def display_players_list_length(players_list):
        print('Nombre de joueurs importés: ', len(players_list))

# FONCTIONS DE SAISIE DE DONNEES
    @staticmethod
    def input_tour_name():
        t_name = input('Veuillez entrer le nom du tournoi: ')
        return t_name

    @staticmethod
    def input_tour_rounds_nr():
        t_rounds_nr_raw = input('Veuillez entrer le nombre de rondes du tournoi: ')
        t_rounds_nr = int(t_rounds_nr_raw)
        return t_rounds_nr

    @staticmethod
    def input_player_name():
        p_name = input('Entrez le nom du joueur: ')
        return p_name

    @staticmethod
    def input_player_elo():
        elo = input('Entrez le classement ELO du joueur: ')
        return elo

    @staticmethod
    def input_player_score_white():
        score_w = input("Entrez le score du joueur BLANCS ('0', '0.5' ou '1'): ")
        return score_w

    @staticmethod
    def input_player_score_black():
        score_b = input("Entrez le score du joueur NOIRS ('0', '0.5' ou '1'): ")
        return score_b

    @staticmethod
    def input_user_choice_addition():
        user_choice = input("Confirmer l'ajout? Y/N: ")
        return user_choice

    @staticmethod
    def input_user_choice_deletion():
        user_choice = input("Confirmer la suppression? Y/N: ")
        return user_choice
