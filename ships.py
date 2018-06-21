import generators
import engines
import warpDrives


def gcbs_371(pilotId, ownerId):
	return {
		'pilotId' : pilotId, #Id of the player piloting the ship:
		'ownerId' : ownerId, #Id of the player who owns the ship. Usually the same, but players will be able to fly other players ships without owning them.
		'type' : 'Ship',
		'class' : "BattleShip",
		'model' : "GCBS_371",
		'name' : "",
		'primaryEngineRoom' : gcbsPrimaryEngineRoom(),
		'leftAuxEngineRoom' : gcbsAuxEngineRoom(),
		'rightAuxEngineRoom' : gcbsAuxEngineRoom(),
		'warpDriveRoom' : gcbsWarpDriveRoom(),
		'powerRoom' : gcbsPowerRoom(),
		'leftHanger' : gcbsHanger(),
		'rightHanger' : gcbsHanger(),
		'cargoBay' : cargoBay(),
	}

def gcbsPrimaryEngineRoom():
	return {
		'maxHealth' : 10000, 
		'damage' : 0,
		'personell' : [],
		'engine' : engines.vmr(),
	}

def gcbsAuxEngineRoom():
	return {
		'maxHealth' : 5000, 
		'damage' : 0,
		'personell' : [],
		'engine' : engines.hdlt(),
	}

def gcbsWarpDriveRoom():
	return {
		'maxHealth' : 5000, 
		'damage' : 0,
		'personell' : [],
		'warpDrive' : warpDrives.wde480(),
	}

def gcbsPowerRoom():
	return {
		'maxHealth' : 5000, 
		'damage' : 0,
		'personell' : [],
		'generator' : generators.dd_fg_955(),
	}

def gcbsHanger():
	hanger = {
		'maxHealth' : 10000,
		'damage' : 0,
		'personell' : [],
	}
	for bay in range(10):
		bay = "bay"+str(bay+1).zfill(2)
		hanger.update(
			{
				bay : {
					'maxHealth' : 500,
					'damage' : 0,
					'type' : "Cargo Bay",
					'class' : "Fighter",
					'fighter' : {},
				}
			})
	return hanger

def cargoBay():
	bays = {
		'maxHealth' : 50000, 
		'damage' : 0, 
		'personnel' : []
	}
	a = {'sm' : 10, 'md' : 20, 'lg' : 10, 'xl' : 5}
	for key, value in a.iteritems():
		for a in range(value):
			bays.update( {key+"Bay"+str(a+1).zfill(2) : {'maxHealth' : 1000, 'damage' : 0, 'type' : "Cargo Bay", 'class' : key.upper(), 'object' : {} } })
	return bays	