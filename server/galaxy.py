import random
import string
from random import randrange, uniform
from dbOps import dbInsert



def idGenerator(size):
	return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(size))

# LETS CREATE A GALAXY #
# 100x100 sectors
# Each sector is 100Au across or 14,959,787,100km Basically 15 billion Km across

# Solar unites for measurements 
g = 6.67384 * pow(10,-11) # Gravitational constant
su = 1.9891 * pow(10, 30) # Mass of our Sun, using this as a reference for other stars of different sizes.
au = 149597871 # Astronomical Unit in km
sr = 6.955 * pow(10,8) #Solar Radii in meters, Don't forget that this number needs to be divided by 1000 for our scale.
em = 6.972* pow(10,24) # Earth's mass, in kg
c =  299792458 # Speed of light in m/s
ed = 12742 #Diameter of Earth in km
er = ed/2
	
	
def sectors():
	starCount = 0

	stars = {
	'O' : {
		'starClass' : "0",
		'starColor' : "Blue",
		'starMass' : uniform( 16, 150 ) * (1.9891 * pow(10, 30)),
		'starRadii' : int(uniform( 6.6, 20 ) * 696300),
		'starLuminosity' : randrange( 30000, 500000 )
		},
	'B' : {
		'starClass' : "B",
		'starColor' : "Blue White",
		'starMass' : uniform( 2.1, 16 ) * (1.9891 * pow(10, 30)),
		'starRadii' : int(uniform( 1.8, 6.6 ) * 696300),
		'starLuminosity' : uniform( 25, 30000 )
		},
	'A' : {
		'starClass' : "A",
		'starColor' : "White",
		'starMass' : uniform( 1.4, 2.1 ) * (1.9891 * pow(10, 30)),
		'starRadii' : int(uniform( 1.4, 1.8 ) * 696300),
		'starLuminosity' : uniform( 5, 25 )
		},
	'F' : {
		'starClass' : "F",
		'starColor' : "Yellow White",
		'starMass' : uniform( 1.04, 1.4 ) * (1.9891 * pow(10, 30)),
		'starRadii' : int(uniform( 1.15, 1.4 ) * 696300),
		'starLuminosity' : uniform( 1.5, 5 )
		},
	'G' : {
		'starClass' : "G",
		'starColor' : "Yellow",
		'starMass' : uniform( 0.8, 1.4 ) * (1.9891 * pow(10, 30)),
		'starRadii' : int(uniform( 0.96, 1.15 ) * 696300),
		'starLuminosity' : uniform( 0.6, 1.5 )
		},
	'K' : {
		'starClass' : "K",
		'starColor' : "Orange",
		'starMass' : uniform( 0.45, 0.8 ) * (1.9891 * pow(10, 30)),
		'starRadii' : int(uniform( 0.7, 0.96 ) * 696300),
		'starLuminosity' : uniform( 0.08, 0.6 )
		},
	'M' : {
		'starClass' : "M",
		'starColor' : "Red",
		'starMass' : uniform( 0.75, 0.45 ) * (1.9891 * pow(10, 30)),
		'starRadii' : int(uniform( 0.05, 0.7 ) * 696300),
		'starLuminosity' : uniform( 0.0001, 0.08 )
		}
	}
	
	
	
	planets = {
	'Terrestrial' : {
		'planetClass' : "Terrestrial",
		'planetMass' : uniform( 0.25, 15 ) * (6.972 * pow(10, 24)),
		}
	}
	

	def system():
		systemChance = randrange( 0,100 )
		if systemChance < 95:
			# Lets create a solar system.
			# First we will start with creating the star.
			# Pick the location
			starX, starY = randrange( 6959787100, 8959787100 ), randrange( 6959787100, 8959787100 )  # 4,959,787,100, 10,959,787,100 Star can't be created within 4 bil km of the border of the sector.
			# Now pick the type of star:
			choose_star = random.randrange(1,1000)
			print choose_star
			star = ""
			if choose_star <= 750:
				star = stars['F']
				print "f"
			elif choose_star >=751 and choose_star <= 870:
				star = stars['G']
				print "g"
			elif choose_star >=871 and choose_star <= 945:
				star = stars['K']
				print "k"
			elif choose_star >=946 and choose_star <= 975:
				star = stars['M']
				print "m"
			elif choose_star >=976 and choose_star <= 981:
				star = stars['A']
				print "a"
			elif choose_star >= 982 and choose_star <= 985:
				star = stars['B']
				print "b"
			elif choose_star >= 986 and choose_star <= 990:
				star = stars['O']
				print "o"
			elif choose_star >= 991:
				print choose_star
				return ""

			star.update( {
				'name' : idGenerator(5),
				'habitalMin' : int( (149597871 * star['starLuminosity']) * .75 ),
				'habitalMax' : int( (149597871 * star['starLuminosity']) * 1.25 ),
				'x' : int(starX),
				'y' : int(starY)
			} )
			
			# find the max distance to either edge of the secor.
			min = ( 14959787100 - starX) + (star['starRadii'] *2)
			planetCount = randrange( 3,8 )
			planets = []
			for a in range(planetCount):
				size = uniform( .35, 100 )
				planetRadii = size * er
				planetMass = size * em
				planetX = uniform( (min * 1.1), 13959787100 ) + planetRadii
				planetY = starY
				planets.append( {'name' : idGenerator(4), 'x' : planetX, 'y' : planetY, 'planetRadii' : planetRadii, 'planetMass' : planetMass })
				
				# print planetX
				
			star.update( {'planets' : planets} )
			
			
			return star
		print "Empty System"
		return ""	
			
			
	for x, a in enumerate(range(10)):
		for y, b in enumerate(range(10)):
			sector = {
				'name' : idGenerator(6), # string
				'x' : x, # int
				'y' : y, # int
				'owner' : "", # ObjectId
				'constellation' : system(),
				'stars' : [], # Array of objects
				'planets' : [], # Array of objects
				'players' : [], # Array of objects
				'ships' : [], # Array of objects
				}
			print sector
				
			dbInsert( 'system' , sector )
	print starCount
			
			
			
			
sectors()