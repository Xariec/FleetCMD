
from dbOps import dbQueryOne

def navMap(player):
	player = dbQueryOne( 'players', {'playerName' : player } )
	