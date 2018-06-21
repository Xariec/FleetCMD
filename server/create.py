import string
import random

from random import randrange
from dbOps import ts, dbInsert, dbQueryOne, dbUpdate
from objTemplates import starterBattleShip

#
def idGenerator(size):
	return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(size))
	
def randomSize():	
	pass

def sectors():
	for x, a in enumerate(range(100)):
		for y, b in enumerate(range(100)):
			sector = {
				'name' : idGenerator(4), # string
				'x' : x, # int
				'y' : y, # int
				'owner' : "", # ObjectId
				'stars' : [], # Array of objects
				'planets' : [], # Array of objects
				'players' : [], # Array of objects
				'ships' : [], # Array of objects
				}
			dbInsert('vinco', sector)



def startSector(user):
	sector = dbQueryOne( 'system', {'x' : 5, 'y' : 5} )
	pX, pY = 500000,500000
	for a in sector['planets']:
		print a['name']
		if a['name'] == "7H2T":
			pX = a['x']+planetRadii+10000
			pY = a['y']+planetRadii+10000
	sector['players'].append(user)
	dbUpdate( 'system', {'_id' : sector['_id']}, sector )
	return {'sector' : sector['_id'], 'x' : pX, 'y' : pY}

	# vacant = dbQueryOne( 'system', {'x' : randrange(0, 10), 'y' : randrange(0, 10)} )
	# while vacant['owner']:
		# vacant = dbQueryOne( 'system', {'x' : randrange(0, 10), 'y' : randrange(0, 10)} )
	# return vacant['_id']
	
def quickStats(obj):
	power = (int(obj['generator']['object']['currentDeuterium'])*float(obj['generator']['object']['effiency'])*5)
	fuel = (float(obj['generator']['object']['currentDeuterium'])/float(obj['generator']['object']['deuteriumCapacity']))
	speed = obj['engine']['object']['maxThrust']
	maxHealth = 0
	dmg = 0
	for key, value in obj.iteritems():
		if type(value) is dict:
			for k, v in value.iteritems():
				if v and type(v) is dict:
					for l, w in v.iteritems():
						if l == "maxHealth":
							maxHealth += v[l]
						if l == "dmg":
							dmg += v[l]
				if k == "maxHealth":
					maxHealth += value[k]
				if k == "dmg":
					dmg += value[k]
		if key == "maxHealth":
			maxHealth += obj[key]
		if key == "dmg":
			dmg += obj[key]
	quick_stats = {'power' : power, 'fuel' : fuel, 'speed' : speed, 'health' : (((maxHealth - dmg)/maxHealth)*100) }
			
	return quick_stats
	
def gf_37Default():
	fighter = dbQueryOne( 'objects', {'model' : "GF-37"} )
	engine = dbQueryOne( 'objects', {'model' : "Magnetoplasmadynamic Thruster"} )
	generator = dbQueryOne( 'objects', {'model' : "DD-FG-40"} )
	warpDrive = dbQueryOne( 'objects', {'model' : "WDE-120"} )
	#Power Costs thus far --
		# engine - 200Kw @ 100% thrust or 10,000 m/s 3.33~ % speed of light
		# base Ship - 25KW 
		# Warp - charge based on distance calculated, will max out generator till charge is achieved. Must be caulculated on the fly.
	
	
	fighter['engine'].update( { 'object' : engine} )
	fighter['generator'].update( {'object' : generator} )
	fighter['warp'].update( {'object' : warpDrive} )
	fighter.update( {'quickStats' : quickStats(fighter)} )


def player(obj):
	p = {
	'primaryShip' : gf_37Default(), #ObjectId
	'sector' : startSector(),
	}
	return dbInsert( 'players', p )
	
	
	
# if __name__ == "__main__":
	# gf_37Default()