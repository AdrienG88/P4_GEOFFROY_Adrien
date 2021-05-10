from tinydb import TinyDB, Query
db = TinyDB('db.json')
players_table = db.table('players')
tournaments_table = db.table('tournaments')


class View:
    def __init__(self):
        self.db = db

    # FONCTIONS D'AFFICHAGE DES MENUS

    def display_main_menu(self):
        # defines all options available in main menu
        main_menu = dict()
        main_menu['1'] = 'Menu creation'
        main_menu['2'] = 'Menu tournoi'
        main_menu['3'] = 'Menu recherche'
        main_menu['4'] = 'Menu rapports'
        main_menu['5'] = 'Quitter le programme'

        options = main_menu.keys()
        print('***********************************************\nMENU PRINCIPAL:')
        for entry in options:
            print(entry, main_menu[entry])

        selection = input('***********************************************\nChoisissez une option: ')
        return selection

    def display_creation_menu(self):
        # defines all options available in creation menu
        creation_menu = dict()
        creation_menu['1'] = 'Ajouter un tournoi'
        creation_menu['2'] = 'Ajouter un joueur'
        creation_menu['3'] = 'Ajouter les joueurs au tournoi'
        creation_menu['4'] = 'Menu principal'

        options = creation_menu.keys()
        print('***********************************************\nMENU TOURNOI:')
        for entry in options:
            print(entry, creation_menu[entry])

        selection = input('***********************************************\nChoisissez une option: ')
        return selection

    def display_tournament_menu(self):
        # defines all options available in creation menu
        tournament_menu = dict()
        tournament_menu['1'] = 'Charger le tournoi'
        tournament_menu['2'] = 'Ajouter une ronde'
        tournament_menu['3'] = 'Ajouter les joueurs au tournoi'
        tournament_menu['4'] = 'Menu principal'

        options = tournament_menu.keys()
        print('***********************************************\nMENU TOURNOI:')
        for entry in options:
            print(entry, tournament_menu[entry])

        selection = input('***********************************************\nChoisissez une option: ')
        return selection

    def display_search_menu(self):
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

    def display_reports_menu(self):
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
    def display_menu_options(self, length):
        print('\n***********************************************\nVeuillez choisir une option entre 1 et', str(length))

    # METHODES D'AFFICHAGE DES RONDES

    def display_player_ratings(self, player_ratings):
        print('CLASSEMENT DES PARTICIPANTS:\n Nom  ELO  score')
        for i in range(0, len(player_ratings)):
            print(player_ratings[i][0].name, player_ratings[i][0].elo, player_ratings[i][1])

    def display_round_matches(self, player_ratings):
        print('\nMATCHES DE LA RONDE: ')
        for i in range(0, len(player_ratings), 2):
            print(player_ratings[i][0].name, "contre", player_ratings[i + 1][0].name)

    def input_round_matches(self, i, player_ratings):
            print('MATCH', int(i/2+1))
            print(player_ratings[i][0].name, "contre", player_ratings[i + 1][0].name)



    # FONCTIONS D'AFFICHAGE DES DONNEES DE LA BASE DE DONNEES
    def display_tournament_list(self):
        for tournament in tournaments_table:
            print(tournament)

    def display_player_list(self):
        for player in players_table:
            print(player)

    def search_player_by_name(self, players_table, name):
        joueur = Query()
        result = players_table.search(joueur.Nom == name)
        print(result)

    def search_tournament_by_name(self, tournaments_table, name):
        tour = Query()
        result = tournaments_table.search(tour.Nom == name)
        print(result)

    def display_players_list_length(self, players_list):
        print('Nombre de joueurs importés: ', len(players_list))

# FONCTIONS DE SAISIE DE DONNEES
    def input_tour_name(self):
        t_name = input('Veuillez entrer le nom du tournoi: ')
        return t_name

    def input_tour_rounds_nr(self):
        t_rounds_nr_raw = input('Veuillez entrer le nombre de rondes du tournoi: ')
        t_rounds_nr = int(t_rounds_nr_raw)
        return t_rounds_nr

    def input_player_name(self):
        p_name = input('Entrez le nom du joueur: ')
        return p_name

    def input_player_elo(self):
        elo = input('Entrez le classement ELO du joueur: ')
        return elo

    def input_player_score_white(self):
        score_w = input("Entrez le score du joueur BLANCS ('0', '0.5' ou '1'): ")
        return score_w

    def input_player_score_black(self):
        score_b = input("Entrez le score du joueur NOIRS ('0', '0.5' ou '1'): ")
        return score_b
