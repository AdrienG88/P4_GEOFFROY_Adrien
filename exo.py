from tinydb import TinyDB, Query
import json

# DEFINITION DES CLASSES ET METHODES AFFERENTES
class Player:
    def __init__(self, nom, elo, score):
        self.nom = nom
        self.elo = elo
        self.score = score

    def to_json(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__))


class Tournament:
    def __init__(self, nom, nb_rondes, rondes):
        self.nom = nom
        self.nb_rondes = nb_rondes
        self.rondes = rondes

    def to_json(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__))


class Round:
    def __init__(self, nom, matches):
        self.nom = nom
        self.matches = matches


# DECLARATION DES VARIABLES GLOBALES
db = TinyDB('db2.json')
rondes = list()
joueurs = list()
r_joueurs = list()
tournament = Tournament('TOURNOI_TEST', 4, rondes)

table = db.table('tournament')
TinyDB.DEFAULT_TABLE = 'tournament'

players_table = db.table('players')
serialized_players = players_table.all()


def create_player_instances(joueurs):
    for i in range(0, len(serialized_players)):
        player = Player(serialized_players[i]['nom'],
                        serialized_players[i]['elo'],
                        serialized_players[i]['score']
                       )
        joueurs.append(player)
        print(player.nom, player.elo, player.score)


create_player_instances(joueurs)


# INSTANCIATION DE CLASSE PLAYER DES JOUEURS
#for row in db.table('players'):




# SERIALISATION DES INSTANCES DE CLASSE JOUEUR
# players_table = db.table('players')
# serialized_players = players_table.all()
'''
for i in range(0, len(players_table)):
    


def serialize_players():
    global joueurs
    print(len(db.table('players')))
    for row in db.table('players'):
        joueurs.append(row)
    return joueurs


joueurs = serialize_players()
print('JOUEURS: ', joueurs)
'''

# FONCTION DE CREATION DES ITEMS DES MATCHES
def add_scores_for_round_list(joueurs):
    r_joueurs = list()
    for i in range(0, len(joueurs)):
        r_joueur = Player(nom=joueurs[i].nom, elo=joueurs[i].elo, score=round_scores[i])
        r_joueurs.append(r_joueur)

    return r_joueurs
########################################################################################################################
# RONDE 1

joueurs.sort(reverse=True, key=lambda x: (x.score, x.elo))
print('CLASSEMENT INITIAL: ')
for i in range(0, len(joueurs)):
    print(joueurs[i].nom, joueurs[i].elo, joueurs[i].score)


#fonction lambda pour classer les joueurs en fonction des matches à venir:
#joueurs[i], joueurs[j] avec i<=len(joueurs)/2 et j = i + len(joueurs)/2

# MATCHES DU ROUND1
print('\nMATCHES DU ROUND1: ')
print(joueurs[0].nom, ' - ', joueurs[1].nom)
print(joueurs[2].nom, ' - ', joueurs[3].nom)
print(joueurs[4].nom, ' - ', joueurs[5].nom)
print(joueurs[6].nom, ' - ', joueurs[7].nom)

# SAISIE DES RESULTATS DE LA RONDE1
# A TRANSFORMER EN BOUCLE (de longueur len(players) if len(players)%2 == 0)
# AJOUTER DES TRY EXCEPT (pour éviter les résultats non numériques en saisie)
# print('\nSAISIE DES RESULTATS DE LA RONDE1: ')
'''

print(joueurs[0].nom, 'contre', joueurs[1].nom)
resultat1 = input('Entrez le résultat de ' + joueurs[0].nom + ': ')
resultat2 = input('Entrez le résultat de ' + joueurs[1].nom + ': ')
print(joueurs[2].nom, 'contre', joueurs[3].nom)
resultat3 = input('Entrez le résultat de ' + joueurs[2].nom + ': ')
resultat4 = input('Entrez le résultat de ' + joueurs[3].nom + ': ')
print(joueurs[4].nom, 'contre', joueurs[5].nom)
resultat5 = input('Entrez le résultat de ' + joueurs[4].nom + ': ')
resultat6 = input('Entrez le résultat de ' + joueurs[5].nom + ': ')
print(joueurs[6].nom, 'contre', joueurs[7].nom)
resultat7 = input('Entrez le résultat de ' + joueurs[6].nom + ': ')
resultat8 = input('Entrez le résultat de ' + joueurs[7].nom + ': ')
'''

resultat1 = 0
resultat2 = 1
resultat3 = 0
resultat4 = 1
resultat5 = 0
resultat6 = 1
resultat7 = 1
resultat8 = 0
round_scores = [resultat1, resultat2, resultat3, resultat4, resultat5, resultat6, resultat7, resultat8]

# A TRANSFORMER EN BOUCLE
# Creation des items des matches

create_round_list()

# A TRANSFORMER EN BOUCLE
match1 = (r_joueurs[0], r_joueurs[1])
match2 = (r_joueurs[2], r_joueurs[3])
match3 = (r_joueurs[4], r_joueurs[5])
match4 = (r_joueurs[6], r_joueurs[7])

# RESULTATS DES MATCHES
# ON POURRAIT UTILISER PANDAS POUR PROPOSER DE BEAUX TABLEAUX
print('\nRESULTATS DES MATCHES: ',
      '\n', match1[0].nom, match1[0].score, match1[1].score, match1[1].nom,
      '\n', match2[0].nom, match2[0].score, match2[1].score, match2[1].nom,
      '\n', match3[0].nom, match3[0].score, match3[1].score, match3[1].nom,
      '\n', match4[0].nom, match4[0].score, match4[1].score, match4[1].nom)

# CREATION D'UNE VARIABLE ronde1 qui est ajoutée à rondes pour être stockée dans l'instance de classe Tournament
# une ronde est une liste de tuples de 2 items de classe Player

ronde1 = Round(nom='Ronde1', matches=[match1, match2, match3, match4])
rondes.append(ronde1)

#MISE A JOUR DES RESULTATS DU TOURNOI DANS LA LISTE "joueurs"
for i in range(0, len(round_scores)):
    joueurs[i].score = float(joueurs[i].score)
    joueurs[i].score += float(round_scores[i])

# ON CLASSE LES JOUEURS APRES AVOIR ENTRE LES RESULTATS DU ROUND
joueurs.sort(reverse=True, key=my_function_a)
joueurs.sort(reverse=True, key=my_function_b)
print('\nCLASSEMENT EN FIN DE ROUND: ')
for i in range(0, len(joueurs)):
    print(joueurs[i].nom, joueurs[i].elo, joueurs[i].score)


table.insert(tournament.to_json())

########################################################################################################################
# RONDES 2 à 4
# A BOUCLER en fonction de nb_rondes-1


print('\n\nMATCHES DU ROUND2: ')
print(joueurs[0].nom, ' - ', joueurs[1].nom)
print(joueurs[2].nom, ' - ', joueurs[3].nom)
print(joueurs[4].nom, ' - ', joueurs[5].nom)
print(joueurs[6].nom, ' - ', joueurs[7].nom)

print('\nSAISIE DES RESULTATS DE LA RONDE2: ')

resultat1 = 0
resultat2 = 1
resultat3 = 0
resultat4 = 1
resultat5 = 0
resultat6 = 1
resultat7 = 0
resultat8 = 1
round_scores = [resultat1, resultat2, resultat3, resultat4, resultat5, resultat6, resultat7, resultat8]

# # Creation des items des matches
create_round_list()

# A TRANSFORMER EN BOUCLE
match1 = (r_joueurs[0], r_joueurs[1])
match2 = (r_joueurs[2], r_joueurs[3])
match3 = (r_joueurs[4], r_joueurs[5])
match4 = (r_joueurs[6], r_joueurs[7])

# RESULTATS DES MATCHES
# ON POURRAIT UTILISER PANDAS POUR PROPOSER DE BEAUX TABLEAUX
print('\nRESULTATS DES MATCHES: ',
      '\n', match1[0].nom, match1[0].score, match1[1].score, match1[1].nom,
      '\n', match2[0].nom, match2[0].score, match2[1].score, match2[1].nom,
      '\n', match3[0].nom, match3[0].score, match3[1].score, match3[1].nom,
      '\n', match4[0].nom, match4[0].score, match4[1].score, match4[1].nom)


# CREATION D'UNE VARIABLE ronde2 qui est ajoutée à rondes pour être stockée dans l'instance de classe Tournament
# une ronde est une liste de tuples de 2 items de classe Player
ronde2 = Round(nom='Ronde2', matches=[match1, match2, match3, match4])
rondes.append(ronde2)

#MISE A JOUR DES RESULTATS DU TOURNOI DANS LA LISTE "joueurs"
for i in range(0, len(round_scores)):
    joueurs[i].score = float(joueurs[i].score)
    joueurs[i].score += float(round_scores[i])

# ON CLASSE LES JOUEURS APRES AVOIR ENTRE LES RESULTATS DU ROUND
joueurs.sort(reverse=True, key=lambda x: (x.score, x.elo))
print('\nCLASSEMENT EN FIN DE ROUND: ')
for i in range(0, len(joueurs)):
    print(joueurs[i].nom, joueurs[i].elo, joueurs[i].score)

########################################################################################################################
# RONDES 3
# A BOUCLER en fonction de nb_rondes-1


print('\n\nMATCHES DU ROUND3: ')
print(joueurs[0].nom, ' - ', joueurs[1].nom)
print(joueurs[2].nom, ' - ', joueurs[3].nom)
print(joueurs[4].nom, ' - ', joueurs[5].nom)
print(joueurs[6].nom, ' - ', joueurs[7].nom)

print('\nSAISIE DES RESULTATS DE LA RONDE3: ')

resultat1 = 0
resultat2 = 1
resultat3 = 1
resultat4 = 0
resultat5 = 1
resultat6 = 0
resultat7 = 1
resultat8 = 0
round_scores = [resultat1, resultat2, resultat3, resultat4, resultat5, resultat6, resultat7, resultat8]

# # Creation des items des matches
create_round_list()

# A TRANSFORMER EN BOUCLE
match1 = (r_joueurs[0], r_joueurs[1])
match2 = (r_joueurs[2], r_joueurs[3])
match3 = (r_joueurs[4], r_joueurs[5])
match4 = (r_joueurs[6], r_joueurs[7])

# RESULTATS DES MATCHES
# ON POURRAIT UTILISER PANDAS POUR PROPOSER DE BEAUX TABLEAUX
print('\nRESULTATS DES MATCHES: ',
      '\n', match1[0].nom, match1[0].score, match1[1].score, match1[1].nom,
      '\n', match2[0].nom, match2[0].score, match2[1].score, match2[1].nom,
      '\n', match3[0].nom, match3[0].score, match3[1].score, match3[1].nom,
      '\n', match4[0].nom, match4[0].score, match4[1].score, match4[1].nom)


# CREATION D'UNE VARIABLE ronde2 qui est ajoutée à rondes pour être stockée dans l'instance de classe Tournament
# une ronde est une liste de tuples de 2 items de classe Player
ronde3 = Round(nom='Ronde3', matches=[match1, match2, match3, match4])
rondes.append(ronde3)

#MISE A JOUR DES RESULTATS DU TOURNOI DANS LA LISTE "joueurs"
for i in range(0, len(round_scores)):
    joueurs[i].score = float(joueurs[i].score)
    joueurs[i].score += float(round_scores[i])

# ON CLASSE LES JOUEURS APRES AVOIR ENTRE LES RESULTATS DU ROUND
joueurs.sort(reverse=True, key=lambda x: (x.score, x.elo))
print('\nCLASSEMENT EN FIN DE ROUND: ')
for i in range(0, len(joueurs)):
    print(joueurs[i].nom, joueurs[i].elo, joueurs[i].score)

########################################################################################################################
# RONDE 4
# A BOUCLER en fonction de nb_rondes-1


print('\n\nMATCHES DU ROUND4: ')
print(joueurs[0].nom, ' - ', joueurs[1].nom)
print(joueurs[2].nom, ' - ', joueurs[3].nom)
print(joueurs[4].nom, ' - ', joueurs[5].nom)
print(joueurs[6].nom, ' - ', joueurs[7].nom)

print('\nSAISIE DES RESULTATS DE LA RONDE4: ')

resultat1 = 0
resultat2 = 1
resultat3 = 0.5
resultat4 = 0.5
resultat5 = 0
resultat6 = 1
resultat7 = 1
resultat8 = 0
round_scores = [resultat1, resultat2, resultat3, resultat4, resultat5, resultat6, resultat7, resultat8]

# # Creation des items des matches
create_round_list()

# A TRANSFORMER EN BOUCLE
match1 = (r_joueurs[0], r_joueurs[1])
match2 = (r_joueurs[2], r_joueurs[3])
match3 = (r_joueurs[4], r_joueurs[5])
match4 = (r_joueurs[6], r_joueurs[7])

# RESULTATS DES MATCHES
# ON POURRAIT UTILISER PANDAS POUR PROPOSER DE BEAUX TABLEAUX
print('\nRESULTATS DES MATCHES: ',
      '\n', match1[0].nom, match1[0].score, match1[1].score, match1[1].nom,
      '\n', match2[0].nom, match2[0].score, match2[1].score, match2[1].nom,
      '\n', match3[0].nom, match3[0].score, match3[1].score, match3[1].nom,
      '\n', match4[0].nom, match4[0].score, match4[1].score, match4[1].nom)


# CREATION D'UNE VARIABLE ronde4 qui est ajoutée à rondes pour être stockée dans l'instance de classe Tournament
# une ronde est une liste de tuples de 2 items de classe Player
ronde4 = Round(nom='Ronde4', matches=[match1, match2, match3, match4])
rondes.append(ronde4)

#MISE A JOUR DES RESULTATS DU TOURNOI DANS LA LISTE "joueurs"
for i in range(0, len(round_scores)):
    joueurs[i].score = float(joueurs[i].score)
    joueurs[i].score += float(round_scores[i])

# ON CLASSE LES JOUEURS APRES AVOIR ENTRE LES RESULTATS DU ROUND
joueurs.sort(reverse=True, key=lambda x: (x.score, x.elo))
print('\nCLASSEMENT EN FIN DE TOURNOI: ')
for i in range(0, len(joueurs)):
    print(joueurs[i].nom, joueurs[i].elo, joueurs[i].score)


# SAUVEGARDE DES RESULTATS DU TOURNOI
table.insert(tournament.to_json())

'''

#var = Query()
#data = db.search(var.nom == 'Jacky')
#print(Player(data[0]['nom'], data[0]['elo']))
'''
