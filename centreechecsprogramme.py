from tinydb import TinyDB
from P4_03_controller import Controller

# Database creation if needed.
with open('db.json', 'a') as f:
    print("Base de données en place!")

# Preliminary variable initializations.
db = TinyDB('db.json')
rounds = list()
players = list()
r_players = list()
table = db.table('tournament')
players_table = db.table('players')
serialized_players = players_table.all()

# Main program starts here.
c = Controller()
Controller.main_loop(c)
