import pymongo


from dbOps import dbInsert


year = 31449600




#Engine objects:
empty_engine = {
	'name' : "String",
	'type' : "string", #Defaults : engine
	'objectType' : "string", #Defaults: ['alt, pri'],
	'maxThrust' : int, # integer for max thrust
	'thrust' : int, # integer for current thrust.
	'kwCost' : int, # Kw/Hr cost of operation
	'maxLife' : int, # Maximum operating time unit can function without repairs
	'life' : int, # Seconds unit has been used. Current life can be found by subtracting this from maxLife
	'maxHealth' : int, # Maximum health a unit can have
	'dmg' : int, # damage unit has received. Health is this subtracted from max. Operation requires at least 30% health.
	'overheat' : int, # Max seconds of continued max thrust operation before unit overheats.
	'buildTime' : int, # Time in seconds to take Mechanic to build one.
	'cost' : {
		'iron' : int, # Iron cost to build, repair is a percentage of this number
		'carbon' : int, # Carbon cost to build, repair is a percentage of this number
		'water' : int, # water cost to build, repair is a percentage of this number
		'silicone' : int, # silicone cost to build, repair is a percentage of this number
		}
	}
	

EIT = {
	'pId' : "",
	'model' : "Electrostatic Ion Thruster",
	'type' : "Engine",
	'objectType' : "ALT",
	'maxThrust' : 20000,
	'thrust' : 0,
	'overheat' : 3000,
	'kwCost' : 60,
	'maxLife' : 3600000,
	'life' : 0,
	'maxHealth' : 5000,
	'dmg' : 0,
	'buildTime' : 72000,
	'cargoSize' : "LG",
	'cost' : {
		'iron' : 5000,
		'carbon' : 2000,
		'water' : 50,
		'silicone' : 2500,
		}
	}
	
XHT = {
	'pId' : "",
	'model' : "Xenon Hall Thruster",
	'type' : "Engine",
	'objectType' : "ALT",
	'maxThrust' : 25000,
	'thrust' : 0,
	'overheat' : 1500,
	'kwCost' : 80,
	'maxLife' : 2520000,
	'life' : 0,
	'maxHealth' : 5000,
	'dmg' : 0,
	'buildTime' : 72000,
	'cargoSize' : "LG",
	'cost' : {
		'iron' : 7000,
		'carbon' : 3000,
		'water' : 100,
		'silicone' : 3500,
		}
	}
HDLT = {
	'pId' : "",
	'model' : "Helicon Double Layer Thruster",
	'type' : "Engine",
	'objectType' : "ALT",
	'maxThrust' : 50000,
	'thrust' : 0,
	'kwCost' : 100,
	'maxLife' : 2160000,
	'life' : 0,
	'maxHealth' : 75000,
	'dmg' : 0,
	'buildTime' : 72000,
	'cargoSize' : "LG",
	'cost' : {
		'iron' : 12000,
		'carbon' : 5000,
		'water' : 150,
		'silicone' : 4000,
		}
	}
MT = {
	'pId' : "",
	'model' : "Magnetoplasmadynamic Thruster",
	'type' : "Engine",
	'objectType' : "PRI",
	'maxThrust' : 100000,
	'thrust' : 0,
	'kwCost' : 200,
	'maxLife' : 3000000,
	'life' : 0,
	'maxHealth' : 10000,
	'dmg' : 0,
	'buildTime' : 72000,
	'cargoSize' : "LG",
	'cost' : {
		'iron' : 30000,
		'carbon' : 10000,
		'water' : 350,
		'silicone' : 6500,
		}
	}
VMR = {
	'pId' : "",
	'model' : "Verible Magnetoplasma Rocket",
	'type' : "Engine",
	'objectType' : "PRI",
	'maxThrust' : 125000,
	'thrust' : 0,
	'kwCost' : 250,
	'maxLife' : 1800000,
	'life' : 0,
	'maxHealth' : 10000,
	'dmg' : 0,
	'buildTime' : 72000,
	'cargoSize' : "LG",
	'cost' : {
		'iron' : 90000,
		'carbon' : 20000,
		'water' : 300,
		'silicone' : 5800,
		}
	}




# Fusion numbers needed
dePermL = int(301107042999999987712) #Atoms of Deuterium per Mili Litre
dFusionMeV = float(2.45) #MeV per reaction
fusionEffiency = float(.4) # Success rate of fusion for all atoms injected. This will be from the effiency of the reactor.
powerMeV = float(((dePermL*.5)*fusionEffiency)*dFusionMeV) #total power generated in one second of fusion
power_WattPerSecond = float( powerMeV/int(6241457006000) ) #Total power in Watts Per Second
mWattPerSecondPerml = float(power_WattPerSecond/1000000) #MegaWatts/second
# print mWattPerSecondPerml

# Reactor requires a minimum of 1ml of Deuterium per second in order to maintain reaction. This generates 23.6391039669 Mw of power per second

# Now, lets get a warp calculated

def warp(distance, warp, reactor, availbleFuel ):
	duration = float( distance/ warp['speed'] ) #How long it takes to complete warp
	fuel_per_second = float( warp['power'] / reactor ) # Cost in liquid Deuterium per second to achieve
	totalFuel = float( duration * fuel_per_second )
	if availbleFuel < totalFuel:
		duration = float(availbleFuel/fuel_per_second)
		distance = float(duration*warp['speed'])
		au = float( distance/ 149598000)
		print "Not enough fuel for jump"
		print "But you can travel as far as %s au" %(int(au))
	else:
		print ((availbleFuel-totalFuel)/availbleFuel)*100
	
	
# warp ( distance in km) (details for warp 1 ) (power output of reactor at idle) (total Fuel available)
# warp((600*149598000), {'speed' : 150000000, 'power' : 20000 }, mWattPerSecondPerml, 450000)


dd_fg_40 = {
	'pId' : "",
	'model' : "DD-FG-40",
	'type' : "Generator",
	'objectType' : "Fusion",
	'effiency' : 0.4,
	'deuteriumCapacity' : 450,
	'currentDeuterium' : 450,
	'maxHealth' : 1000,
	'dmg' : 0,
	'maxLife' : year/3,
	'life' : 0,
	'buildTime' : 72000,
	'cargoSize' : "LG",
	'cost' : {
		'iron' : 90000,
		'carbon' : 20000,
		'water' : 300,
		'silicone' : 5800,
		}
	}
dd_fg_50 = {
	'pId' : "",
	'model' : "DD-FG-50",
	'type' : "Generator",
	'objectType' : "Fusion",
	'effiency' : "0.5",
	'deuteriumCapacity' : 450,
	'currentDeuterium' : 450,
	'maxHealth' : 1000,
	'dmg' : 0,
	'maxLife' : year/3.5,
	'life' : 0,
	'buildTime' : 72000,
	'cargoSize' : "LG",
	'cost' : {
		'iron' : 90000,
		'carbon' : 20000,
		'water' : 300,
		'silicone' : 5800,
		}
	}
dd_fg_65 = {
	'pId' : "",
	'model' : "DD-FG-55",
	'type' : "Generator",
	'objectType' : "Fusion",
	'effiency' : "0.65",
	'deuteriumCapacity' : 600,
	'currentDeuterium' : 600,
	'maxHealth' : 1000,
	'dmg' : 0,
	'maxLife' : year/2,
	'life' : 0,
	'buildTime' : 72000,
	'cargoSize' : "LG",
	'cost' : {
		'iron' : 90000,
		'carbon' : 20000,
		'water' : 300,
		'silicone' : 5800,
		}
	}
dd_fg_700 = {
	'pId' : "",
	'model' : "DD-FG-700",
	'type' : "Generator",
	'objectType' : "Fusion",
	'effiency' : "0.7",
	'deuteriumCapacity' : 600,
	'currentDeuterium' : 600,
	'maxHealth' : 1000,
	'dmg' : 0,
	'maxLife' : year/3.5,
	'life' : 0,
	'buildTime' : 72000,
	'cargoSize' : "LG",
	'cost' : {
		'iron' : 90000,
		'carbon' : 20000,
		'water' : 300,
		'silicone' : 5800,
		}
	}
dd_fg_850 = {
	'pId' : "",
	'model' : "DD-FG-850",
	'type' : "Generator",
	'objectType' : "Fusion",
	'effiency' : "0.85",
	'deuteriumCapacity' : 750,
	'currentDeuterium' : 750,
	'maxHealth' : 1000,
	'dmg' : 0,
	'maxLife' : year/2,
	'life' : 0,
	'buildTime' : 72000,
	'cargoSize' : "LG",
	'cost' : {
		'iron' : 90000,
		'carbon' : 20000,
		'water' : 300,
		'silicone' : 5800,
		}
	}
dd_fg_955 = {
	'pId' : "",
	'model' : "DD-FG-955",
	'type' : "Generator",
	'objectType' : "Fusion",
	'effiency' : "0.95",
	'deuteriumCapacity' : 900,
	'currentDeuterium' : 900,
	'maxHealth' : 1000,
	'dmg' : 0,
	'maxLife' : year,
	'life' : 0,
	'buildTime' : 72000,
	'cargoSize' : "LG",
	'cost' : {
		'iron' : 90000,
		'carbon' : 20000,
		'water' : 300,
		'silicone' : 5800,
		}
	} # Max Power is 4,275 Kw

#Warp Drives for the ship

#effiency is measured in cost of kW per Light year traveled.

# Example (wde_120 = .15(kw/lightyear)*100,000(total/lightyears) = 15,000kW / 890kw = 17
# This would take a dd_fg_40 which has an output of total 900kW at full rest 17 seconds to charge before going into warp.
# If the ship was in motion with decent engines, this it would take 30 seconds to charge before going into warp.
# Also remember there is a recharge time, though the more effective the warp drive, the quicker that is.
# Range is limited charge time of 60 seconds. At rest a dd_gf_40 could charge a wde_120 to create max range of 356,000Lightyears (might rethink some of this)


# Light year = 63,241 AU
# solar system is 100 AU
# Warp = km/s = 1 light year
# Warp 1 = 150,000,000km/s 17.6 Hours
# Warp 2 = 300,000,000km/s 8.78 Hours
# Warp 3 = 600,000,000km/s 4.39 Hours
# Warp 4 = 1,200,000,000Km/s 2.19 Hours
# Warp 5 = 2,400,000,000Km/s 1.06 Hours
# Warp 6 = 4,800,000,000Km/s 32.9 Minutes
# Warp 7 = 9,600,000,000Km/s 16.46 Minutes
# Warp 8 = 19,200,000,000Km/s 8.23 Minutes
# Warp 9 = 38,400,000,000Km/s 4.11 Minutes
# Warp 10 = 76,800,000,000Km/s 1.96 Minutes








wde_120 = {
	'pId' : "",
	'model' : "WDE-120",
	'type' : "Engine",
	'objectType' : "Warp",
	'effiency' : "0.15", # Poorly named
	'recharge' : 60,
	'maxLife' : year/2,
	'maxHealth' : 1000,
	'dmg' : 0,
	'life' : 0,
	'buildTime' : 72000,
	'cargoSize' : "LG",
	'cost' : {
		'iron' : 90000,
		'carbon' : 20000,
		'water' : 300,
		'silicone' : 5800,
		}
	}
wde_240 = {
	'pId' : "",
	'model' : "WDE-240",
	'type' : "Engine",
	'objectType' : "Warp",
	'effiency' : "0.124",
	'recharge' : 30,
	'maxLife' : year/3,
	'maxHealth' : 1000,
	'dmg' : 0,
	'life' : 0,
	'buildTime' : 72000,
	'cargoSize' : "LG",
	'cost' : {
		'iron' : 90000,
		'carbon' : 20000,
		'water' : 300,
		'silicone' : 5800,
		}
	}
wde_480 = {
	'pId' : "",
	'model' : "WDE-480",
	'type' : "Engine",
	'objectType' : "Warp",
	'effiency' : "0.1",
	'recharge' : 15,
	'maxLife' : year/6,
	'maxHealth' : 1000,
	'dmg' : 0,
	'life' : 0,
	'buildTime' : 72000,
	'cargoSize' : "LG",
	'cost' : {
		'iron' : 90000,
		'carbon' : 20000,
		'water' : 300,
		'silicone' : 5800,
		}
	}


gf_37 = {
	'pId' : "",
	'name' : "Falcon",
	'model' : "GF-37",
	'type' : "Ship",
	'objectType' : "Fighter",
	'hull' : 1000,
	'maxHealth' : 1000,
	'dmg' : 0,
	'quickStats' : {
		'power' : 0,
		'speed' : 0,
		'fuel' : 0,
		'health' : 0,
		},
	'cockpit' : {
		'maxHealth' : 500,
		'dmg' : 0,
		'pilot' : {},
		},
	'weapons' : {
		'maxHealth' : 1000,
		'dmg' : 0,
		'cannonLeft' : {},
		'cannonRight' : {},
		'missileLeft1' : {},
		'missileLeft2' : {},
		'missileLeft3' : {},
		'missileRight1' : {},
		'missileRight2' : {},
		'missileRight3' : {},
		'dualLeft' : {},
		'dualRight' : {},
		},
	'engine' : {
		'maxHealth' : 1000,
		'dmg' : 0,
		'type' : "Engine",
		'objectType' : "PRI",
		'object' : {},
		},
	'warp' : {
		'maxHealth' : 1000,
		'dmg' : 0,
		'type' : "Engine",
		'objectType' : "Warp",
		'object' : {},
		},
	'generator' : {
		'maxHealth' : 1000,
		'dmg' : 0,
		'type' : "Generator",
		'objectType' : "Fusion",
		'object' : {},
		},
	'cargoSize' : "NA",
	'buildTime' : 1230000,
	'cost' : {
		'iron' : 90000,
		'carbon' : 20000,
		'water' : 300,
		'silicone' : 5800,
		}
}



def cargoBay():
	bays = {}
	bays.update({'maxHealth' : 50000, 'dmg' : 0, 'personnel' : []})
	for a in range(10):
		a = str(a+1).zfill(2)
		bays.update({'smBay'+a : { 'maxHealth' : 1000, 'dmg' : 0, 'cargoSize' : "SM", 'object' : {} } })
	for b in range(20):
		b = str(b+1).zfill(2)
		bays.update({'mdBay'+b : { 'maxHealth' : 1000, 'dmg' : 0, 'cargoSize' : "MD", 'object' : {} } })
	for c in range(10):
		c = str(c+1).zfill(2)
		bays.update({'lgBay'+c : { 'maxHealth' : 1000, 'dmg' : 0, 'cargoSize' : "LG", 'object' : {} } })
	for d in range(5):
		d = str(d+1).zfill(2)
		bays.update({'xlBay'+d : { 'maxHealth' : 1000, 'dmg' : 0, 'cargoSize' : "XL", 'object' : {} } })
	return bays

	



gcbs_371 = {
	'pId' : "",
	'name' : "",
	'model' : "GCBS_371",
	'type' : "ship",
	'objectType' : "BattleShip",
	'cargoSize' : "NA",
	'maxHealth' : 100000,
	'dmg' : 0,
	'buildTime' : 150000000,
	'cost' : {
		'iron' : 90000,
		'carbon' : 20000,
		'water' : 300,
		'silicone' : 5800,
		},
	'weapons' : {
		'maxHealth' : 1000,
		'dmg' : 0,
		'cannonLeft1' : {
			'maxHealth' : 100,
			'dmg' : 0,
			'type' : "Artillery",
			'objectType' : "Cannon",
			'object' : {}
			},
		'cannonLeft2' : {
			'maxHealth' : 100,
			'dmg' : 0,
			'type' : "Artillery",
			'objectType' : "Cannon",
			'object' : {}
			},
		'cannonLeft3' : {
			'maxHealth' : 100,
			'dmg' : 0,
			'type' : "Artillery",
			'objectType' : "Cannon",
			'object' : {}
			},
		'cannonRight1' : {
			'maxHealth' : 100,
			'dmg' : 0,
			'type' : "Artillery",
			'objectType' : "Cannon",
			'object' : {}
			},
		'cannonRight2' : {
			'maxHealth' : 100,
			'dmg' : 0,
			'type' : "Artillery",
			'objectType' : "Cannon",
			'object' : {}
			},
		'cannonRight3' : {
			'maxHealth' : 100,
			'dmg' : 0,
			'type' : "Artillery",
			'objectType' : "Cannon",
			'object' : {}
			},
		'missileLeft1' : {
			'maxHealth' : 100,
			'dmg' : 0,
			'type' : "Artillery",
			'objectType' : "Missile",
			'object' : {}
			},
		'missileLeft2' : {
			'maxHealth' : 100,
			'dmg' : 0,
			'type' : "Artillery",
			'objectType' : "Missile",
			'object' : {}
			},
		'missileLeft3' : {
			'maxHealth' : 100,
			'dmg' : 0,
			'type' : "Artillery",
			'objectType' : "Missile",
			'object' : {}
			},
		'missileLeft4' : {
			'maxHealth' : 100,
			'dmg' : 0,
			'type' : "Artillery",
			'objectType' : "Missile",
			'object' : {}
			},
		'missileLeft5' : {
			'maxHealth' : 100,
			'dmg' : 0,
			'type' : "Artillery",
			'objectType' : "Missile",
			'object' : {}
			},
		'missileRight1' : {
			'maxHealth' : 100,
			'dmg' : 0,
			'type' : "Artillery",
			'objectType' : "Missile",
			'object' : {}
			},
		'missileRight2' : {
			'maxHealth' : 100,
			'dmg' : 0,
			'type' : "Artillery",
			'objectType' : "Missile",
			'object' : {}
			},
		'missileRight3' : {
			'maxHealth' : 100,
			'dmg' : 0,
			'type' : "Artillery",
			'objectType' : "Missile",
			'object' : {}
			},
		'missileRight4' : {
			'maxHealth' : 100,
			'dmg' : 0,
			'type' : "Artillery",
			'objectType' : "Missile",
			'object' : {}
			},
		'missileRight5' : {
			'maxHealth' : 100,
			'dmg' : 0,
			'type' : "Artillery",
			'objectType' : "Missile",
			'object' : {}
			},
		'dualLeft1' : {
			'maxHealth' : 100,
			'dmg' : 0,
			'type' : "Artillery",
			'objectType' : ['Missile', 'Cannon'],
			'object' : {}
			},
		'dualLeft2' : {
			'maxHealth' : 100,
			'dmg' : 0,
			'type' : "Artillery",
			'objectType' : ['Missile', 'Cannon'],
			'object' : {}
			},
		'dualLeft3' : {
			'maxHealth' : 100,
			'dmg' : 0,
			'type' : "Artillery",
			'objectType' : ['Missile', 'Cannon'],
			'object' : {}
			},
		'dualRight1' : {
			'maxHealth' : 100,
			'dmg' : 0,
			'type' : "Artillery",
			'objectType' : ['Missile', 'Cannon'],
			'object' : {}
			},
		'dualRight2' : {
			'maxHealth' : 100,
			'dmg' : 0,
			'type' : "Artillery",
			'objectType' : ['Missile', 'Cannon'],
			'object' : {}
			},
		'dualRight3' : {
			'maxHealth' : 100,
			'dmg' : 0,
			'type' : "Artillery",
			'objectType' : ['Missile', 'Cannon'],
			'object' : {}
			},
		},
	'engineBay' : {
		'maxHealth' : 50000,
		'dmg' : 0,
		'primaryEngine' : {},
		'altEngine1' : {},
		'altEngine2' : {},
		'warpDrive' : {},
		'personnel' : []
		},
	'powerRoom' : {
		'maxHealth' : 10000,
		'dmg' : 0,
		'reactor' : {},
		'personnel' : []
		},
	'sciLab' : 	{
		'maxHealth' : 10000,
		'dmg' : 0,
		'personnel' : []
		},
	'engineerLab' : {
		'maxHealth' : 10000,
		'dmg' : 0,
		'personnel' : []
		},
	'classroom' : 	{
		'maxHealth' : 10000,
		'dmg' : 0,
		'personnel' : []
		},
	'sickbay' : {
		'maxHealth' : 10000,
		'dmg' : 0,
		'personnel' : []
		},
	'pilotsLounge' : {
		'maxHealth' : 10000,
		'dmg' : 0,
		'personnel' : []
		},
	'leftHanger' : 	{
		'maxHealth' : 10000,
		'dmg' : 0,
		'bay01' : {
			'maxHealth' : 500,
			'dmg' : 0,
			'type' : "Ship",
			'objectType' : "Fighter",
			'object' : {}
			},
		'bay02' : {
			'maxHealth' : 500,
			'dmg' : 0,
			'type' : "Ship",
			'objectType' : "Fighter",
			'object' : {}
			},
		'bay03' : {
			'maxHealth' : 500,
			'dmg' : 0,
			'type' : "Ship",
			'objectType' : "Fighter",
			'object' : {}
			},
		'bay04' : {
			'maxHealth' : 500,
			'dmg' : 0,
			'type' : "Ship",
			'objectType' : "Fighter",
			'object' : {}
			},
		'bay05' : {
			'maxHealth' : 500,
			'dmg' : 0,
			'type' : "Ship",
			'objectType' : "Fighter",
			'object' : {}
			},
		'bay06' : {
			'maxHealth' : 500,
			'dmg' : 0,
			'type' : "Ship",
			'objectType' : "Fighter",
			'object' : {}
			},
		'bay07' : {
			'maxHealth' : 500,
			'dmg' : 0,
			'type' : "Ship",
			'objectType' : "Fighter",
			'object' : {}
			},
		'bay08' : {
			'maxHealth' : 500,
			'dmg' : 0,
			'type' : "Ship",
			'objectType' : "Fighter",
			'object' : {}
			},
		'bay09' : {
			'maxHealth' : 500,
			'dmg' : 0,
			'type' : "Ship",
			'objectType' : "Fighter",
			'object' : {}
			},
		'bay10' : {
			'maxHealth' : 500,
			'dmg' : 0,
			'type' : "Ship",
			'objectType' : "Fighter",
			'object' : {}
			},
		},
	'rightHanger' : {
		'maxHealth' : 10000,
		'dmg' : 0,
		'bay01' : {
			'maxHealth' : 500,
			'dmg' : 0,
			'type' : "Ship",
			'objectType' : "Fighter",
			'object' : {}
			},
		'bay02' : {
			'maxHealth' : 500,
			'dmg' : 0,
			'type' : "Ship",
			'objectType' : "Fighter",
			'object' : {}
			},
		'bay03' : {
			'maxHealth' : 500,
			'dmg' : 0,
			'type' : "Ship",
			'objectType' : "Fighter",
			'object' : {}
			},
		'bay04' : {
			'maxHealth' : 500,
			'dmg' : 0,
			'type' : "Ship",
			'objectType' : "Fighter",
			'object' : {}
			},
		'bay05' : {
			'maxHealth' : 500,
			'dmg' : 0,
			'type' : "Ship",
			'objectType' : "Fighter",
			'object' : {}
			},
		'bay06' : {
			'maxHealth' : 500,
			'dmg' : 0,
			'type' : "Ship",
			'objectType' : "Fighter",
			'object' : {}
			},
		'bay07' : {
			'maxHealth' : 500,
			'dmg' : 0,
			'type' : "Ship",
			'objectType' : "Fighter",
			'object' : {}
			},
		'bay08' : {
			'maxHealth' : 500,
			'dmg' : 0,
			'type' : "Ship",
			'objectType' : "Fighter",
			'object' : {}
			},
		'bay09' : {
			'maxHealth' : 500,
			'dmg' : 0,
			'type' : "Ship",
			'objectType' : "Fighter",
			'object' : {}
			},
		'bay10' : {
			'maxHealth' : 500,
			'dmg' : 0,
			'type' : "Ship",
			'objectType' : "Fighter",
			'object' : {}
			},
		},
	'cargoBay' : cargoBay(),
	'waterStorage' : {
		'maxHealth' : 500,
		'dmg' : 0,
		'capacity' : 10000,
		},
	'deuteriumStorage' : {
		'maxHealth' : 500,
		'dmg' : 0,
		'capacity' : 5000,
		},
	'carbonStorage' : {
		'maxHealth' : 500,
		'dmg' : 0,
		'capacity' : 5000,
		},
	'ironStorage' : {
		'maxHealth' : 500,
		'dmg' : 0,
		'capacity' : 5000,
		},	
	'siliconeStorage' : {
		'maxHealth' : 500,
		'dmg' : 0,
		'capacity' : 5000,
		},	
	}
	
def starterBattleShip():
	
	return gcbs_371
	# for key in battleship['leftHanger']:
		# if 'bay' in key:
			# battleship['leftHanger'][key]['object'].update( gf_37 )
			# print battleship['leftHanger']['health'] - battleship['leftHanger']['dmg']
			
	# for key in battleship['leftHanger']:
		# if 'bay' in key:
			# battleship['leftHanger'].update({ key : gf_37})
	# for key in battleship['rightHanger']:
		# if 'bay' in key:
			# battleship['rightHanger'].update({ key : gf_37})
	# return dbInsert( 'ships', battleship )

	
# objects = [EIT,XHT,HDLT,MT,VMR,dd_fg_40,dd_fg_50,dd_fg_65,dd_fg_700,dd_fg_850,dd_fg_955,wde_120,wde_240,wde_480,gf_37,gcbs_371]


# if __name__ == "__main__":
	# for a in objects:
		# dbInsert( 'objects', a )


