from tinydb import TinyDB
from P4_03_controller import Controller

# DECLARATION DES VARIABLES GLOBALES
db = TinyDB('db.json')
rounds = list()
players = list()
r_players = list()
# tournament = Tournament('TOURNOI_TEST', 4, rounds)

table = db.table('tournament')
players_table = db.table('players')
serialized_players = players_table.all()


c = Controller()
Controller.main_loop(c)
