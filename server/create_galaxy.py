import random
import pymongo
from pymongo import MongoClient
import time
import string
import datetime
import math


db = MongoClient('localhost', 27017).game

#                    Global Variables

# Set the time variables
now = datetime.datetime.now()  # Gets the current time.
day_of_year = datetime.datetime.now().timetuple().tm_yday
# convert the time to an integer we can use for checking how much time has passed.
days = (now.year * 365) + day_of_year + (now.year/4)
hours = days * 24 + now.hour
minutes = hours *60 + now.minute
seconds = minutes * 60 + now.second # Seconds, fairly accurate depiction of time since the year of 0001
seconds = 0

# Solar unites for measurements 
g = 6.67384 * math.pow(10,-11) # Gravitational constant
su = 1.9891 * math.pow(10, 30) # Mass of our Sun, using this as a reference for other stars of different sizes.
au = 149597871 # Astronomical Unit in km
sr = 6.955 * math.pow(10,8) #Solar Radii in meters, Don't forget that this number needs to be divided by 1000 for our scale.
em = 6.972*math.pow(10,24) # Earth's mass, in kg
c =  299792458 # Speed of light in m/s
ed = 12742 #Diameter of Earth in km
	
def id_generator_planet(size=8, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for x in range(size))
	
def id_generator_star(size=5, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for x in range(size))



planet_classes = ('Terrestrial', 'Desert', 'Iron', 'Ocean', 'Gas', 'Ice')


iron_ore = {'Terrestrial' : random.randint(10,100), 'Desert' : random.randint(10,100), 'Gas' : random.randint(1, 2), 'Ice' : random.randint(5,30), 'Iron' : random.randint(5,30), 'Ocean' : random.randint(5,30)}

carbon_ore = {'Terrestrial' : random.randint(10,100), 'Desert' : random.randint(10,100), 'Gas' : random.randint(1, 2), 'Ice' : random.randint(5,30), 'Iron' : random.randint(5,30), 'Ocean' : random.randint(5,30)}

oxygen_ore = {'Terrestrial' : random.randint(10,100), 'Desert' : random.randint(10,100), 'Gas' : random.randint(1, 2), 'Ice' : random.randint(5,30), 'Iron' : random.randint(5,30), 'Ocean' : random.randint(5,30)}

h2o_ore = {'Terrestrial' : random.randint(10,100), 'Desert' : random.randint(10,100), 'Gas' : random.randint(1, 2), 'Ice' : random.randint(5,30), 'Iron' : random.randint(5,30), 'Ocean' : random.randint(5,30)}

deuterium_ore = {'Terrestrial' : random.randint(10,100), 'Desert' : random.randint(10,100), 'Gas' : random.randint(1, 2), 'Ice' : random.randint(5,30), 'Iron' : random.randint(5,30), 'Ocean' : random.randint(5,30)}




star_classes = ('O', 'B', 'A', 'F', 'G', 'K', 'M')

star_color = {'O' : "Blue", 'B' : "Blue White", 'A' : "White", 'F' : "Yellow White", 'G' : "Yello", 'K' : "Orange", 'M' : "Red"}

star_solar_mass = {'O' : "16,150", 'B' : "2.1,16", 'A' : "1.4,2.1", 'F' : "1.04,1.4", 'G' : "0.8,1.4", 'K' : ".45,.8", 'M' : ".075,.45"}

star_solar_radii = {'O' : "6.6,20", 'B' : "1.8,6.6", 'A' : "1.4,1.8", 'F' : "1.15,1.4", 'G' : ".96,1.15", 'K' : ".7,.96", 'M' : ".05,.7"}


star_solar_luminosity = {'O' : "30000,500000", 'B' : "25,30000", 'A' : "5,25", 'F' : "1.5,5", 'G' : ".6,1.5", 'K' : ".08,.6", 'M' : ".0001,.08"}

star_chance = {'.00003' : "O", '.125' : "B", '.625' : "A", '3.03' : "F", '7.5' : "G", '12' : "K", '76' : "M"}


	


def planet(planet_count, star_radii, mass, habbital_zone_min, habbital_zone_max, s_id, x , y, system_size):
	distance = 0
	count = 0
	for a in range(planet_count):
		distance = int(random.uniform(.25, 10)*au)
		if distance > star_radii and distance < habbital_zone_min and distance <= system_size:
			choice = planet_classes[random.randrange(1,2)]
			name = id_generator_planet()
			size = random.uniform(.25,15)
			planet_mass = size*em
			planet_diameter = size*ed
			if planet_diameter > 10*ed:
				planet_type = choice
				# print planet_type
				r = distance * 1000 # Need actual distance for mapping orbits, this converts it into meters.
				v = math.sqrt((g*mass)/r)
				op = 2*math.pi*math.sqrt(math.pow(r,3)/(g*mass)) 
				iron = int(planet_diameter*iron_ore[planet_type])
				carbon = int(planet_diameter*carbon_ore[planet_type])
				oxygen = int(planet_diameter*oxygen_ore[planet_type])
				h2o = int(planet_diameter*h2o_ore[planet_type])
				deuterium = int(planet_diameter*deuterium_ore[planet_type])
				area = int((planet_diameter/random.randint(5,10)))
				planet_type = "Giant "+choice
				db.universe.insert({'name' : name, 'x_pos' : x+distance, 'y_pos' : y, 'area' : area, 'item' : "planet", 'p_id' : s_id, 'iron' : iron, 'carbon' : carbon, 'oxygen' : oxygen, 'h2o' : h2o, 'deuterium' : deuterium, 'type' : planet_type, 'velocity' : v, 'created' : seconds, 'distance' : distance, 'op' : op})
			else:
				planet_type = choice
				# print planet_type
				r = distance * 1000 # Need actual distance for mapping orbits, this converts it into meters.
				v = math.sqrt((g*mass)/r)
				op = 2*math.pi*math.sqrt(math.pow(r,3)/(g*mass)) 
				iron = int(planet_diameter*iron_ore[planet_type])
				carbon = int(planet_diameter*carbon_ore[planet_type])
				oxygen = int(planet_diameter*oxygen_ore[planet_type])
				h2o = int(planet_diameter*h2o_ore[planet_type])
				deuterium = int(planet_diameter*deuterium_ore[planet_type])
				area = int((planet_diameter/random.randint(5,10)))
				db.universe.insert({'name' : name, 'x_pos' : x+distance, 'y_pos' : y, 'area' : area, 'item' : "planet", 'p_id' : s_id, 'iron' : iron, 'carbon' : carbon, 'oxygen' : oxygen, 'h2o' : h2o, 'deuterium' : deuterium, 'type' : planet_type, 'velocity' : v, 'created' : seconds, 'distance' : distance, 'op' : op})
		elif distance > star_radii and distance >= habbital_zone_min and distance <= habbital_zone_max and distance <= system_size:
			choice = planet_classes[0]
			name = id_generator_planet()
			size = random.uniform(.25,15)
			planet_mass = size*em
			planet_diameter = size*ed
			if planet_diameter > 10*ed:
				planet_type = choice
				# print planet_type
				r = distance * 1000 # Need actual distance for mapping orbits, this converts it into meters.
				v = math.sqrt((g*mass)/r)
				op = 2*math.pi*math.sqrt(math.pow(r,3)/(g*mass)) 
				iron = int(planet_diameter*iron_ore[planet_type])
				carbon = int(planet_diameter*carbon_ore[planet_type])
				oxygen = int(planet_diameter*oxygen_ore[planet_type])
				h2o = int(planet_diameter*h2o_ore[planet_type])
				deuterium = int(planet_diameter*deuterium_ore[planet_type])
				area = int((planet_diameter/random.randint(5,10)))
				planet_type = "Giant "+choice
				db.universe.insert({'name' : name, 'x_pos' : x+distance, 'y_pos' : y, 'area' : area, 'item' : "planet", 'p_id' : s_id, 'iron' : iron, 'carbon' : carbon, 'oxygen' : oxygen, 'h2o' : h2o, 'deuterium' : deuterium, 'type' : planet_type, 'velocity' : v, 'created' : seconds, 'distance' : distance, 'op' : op})
			else:
				planet_type = choice
				# print planet_type
				r = distance * 1000 # Need actual distance for mapping orbits, this converts it into meters.
				v = math.sqrt((g*mass)/r)
				op = 2*math.pi*math.sqrt(math.pow(r,3)/(g*mass)) 
				iron = int(planet_diameter*iron_ore[planet_type])
				carbon = int(planet_diameter*carbon_ore[planet_type])
				oxygen = int(planet_diameter*oxygen_ore[planet_type])
				h2o = int(planet_diameter*h2o_ore[planet_type])
				deuterium = int(planet_diameter*deuterium_ore[planet_type])
				area = int((planet_diameter/random.randint(5,10)))
				db.universe.insert({'name' : name, 'x_pos' : x+distance, 'y_pos' : y, 'area' : area, 'item' : "planet", 'p_id' : s_id, 'iron' : iron, 'carbon' : carbon, 'oxygen' : oxygen, 'h2o' : h2o, 'deuterium' : deuterium, 'type' : planet_type, 'velocity' : v, 'created' : seconds, 'distance' : distance, 'op' : op})
		elif distance > star_radii and distance > habbital_zone_max and distance < system_size:
			choice = planet_classes[random.randrange(2,5)]
			name = id_generator_planet()
			size = random.uniform(.25,350)
			planet_mass = size*em
			planet_diameter = size*ed
			if planet_diameter > 10*ed:
				planet_type = choice
				# print planet_type
				r = distance * 1000 # Need actual distance for mapping orbits, this converts it into meters.
				v = math.sqrt((g*mass)/r)
				op = 2*math.pi*math.sqrt(math.pow(r,3)/(g*mass)) 
				iron = int(planet_diameter*iron_ore[planet_type])
				carbon = int(planet_diameter*carbon_ore[planet_type])
				oxygen = int(planet_diameter*oxygen_ore[planet_type])
				h2o = int(planet_diameter*h2o_ore[planet_type])
				deuterium = int(planet_diameter*deuterium_ore[planet_type])
				area = int((planet_diameter/random.randint(5,10)))
				planet_type = "Giant "+choice
				db.universe.insert({'name' : name, 'x_pos' : x+distance, 'y_pos' : y, 'area' : area, 'item' : "planet", 'p_id' : s_id, 'iron' : iron, 'carbon' : carbon, 'oxygen' : oxygen, 'h2o' : h2o, 'deuterium' : deuterium, 'type' : planet_type, 'velocity' : v, 'created' : seconds, 'distance' : distance, 'op' : op})
			else:
				planet_type = choice
				# print planet_type
				r = distance * 1000 # Need actual distance for mapping orbits, this converts it into meters.
				v = math.sqrt((g*mass)/r)
				op = 2*math.pi*math.sqrt(math.pow(r,3)/(g*mass)) 
				iron = int(planet_diameter*iron_ore[planet_type])
				carbon = int(planet_diameter*carbon_ore[planet_type])
				oxygen = int(planet_diameter*oxygen_ore[planet_type])
				h2o = int(planet_diameter*h2o_ore[planet_type])
				deuterium = int(planet_diameter*deuterium_ore[planet_type])
				area = int((planet_diameter/random.randint(5,10)))
				db.universe.insert({'name' : name, 'x_pos' : x+distance, 'y_pos' : y, 'area' : area, 'item' : "planet", 'p_id' : s_id, 'iron' : iron, 'carbon' : carbon, 'oxygen' : oxygen, 'h2o' : h2o, 'deuterium' : deuterium, 'type' : planet_type, 'velocity' : v, 'created' : seconds, 'distance' : distance, 'op' : op})

		
def star(chosen_class, x, y, p_id):
	name = id_generator_star()
	star_class = star_classes[chosen_class]
	color = star_color[star_class]
	solar_mass = star_solar_mass[star_class].split(',')
	star_mass = random.uniform(float(solar_mass[0]),float(solar_mass[1]))*su
	solar_radii = star_solar_radii[star_class].split(',')
	star_radii = random.uniform(float(solar_radii[0]),float(solar_radii[1]))*sr
	solar_luminosity = star_solar_luminosity[star_class].split(',')
	star_luminosity = random.uniform(float(solar_luminosity[0]),float(solar_luminosity[1]))
	star_habbital_zone_min = au*star_luminosity*.75
	star_habbital_zone_max = au*star_luminosity*1.25
	system_size = random.uniform(1,10)*au
	planet_chance = random.randrange(0,3)
	s_id = db.universe.insert({'name' : name, 'x_pos' : x, 'y_pos' : y, 'item' : "star", 'p_id' : p_id, 'type' : star_class, 'color' : color, 'mass' : star_mass, 'radii' : star_radii, 'luminosity' : star_luminosity, 'habbital_min' : star_habbital_zone_min, 'habbital_max' : star_habbital_zone_max, 'created' : seconds, 'diameter' : math.pow(star_radii,2), 'system_size' : system_size})
	planet(random.randrange(0,10)*planet_chance,star_radii, star_mass, star_habbital_zone_min, star_habbital_zone_max, s_id, x, y, system_size)

def zeus():
	name = "Sun"
	item = "star" 
	x = 2629742
	y = 2629742
	solar_system_size = 590000
	star_type = "O"
	star_color = "Yellow White"
	diameter = sr*2
	mass = su
	p_id = db.universe.insert({'name' : name, 'item' : item , 'x_pos' : x, 'y_pos' : y, 'size' : solar_system_size, 'type' : star_type, 'color' : star_color, 'diameter' : diameter, 'created' : seconds})
	
	for planet in ((580 , "Mercury", 4879, planet_classes[0],1),
					(1080,"Venus",12100, planet_classes[0],1),
					(1500,"Earth", 12742, planet_classes[1],1),
					(2280,"Mars", 6792, planet_classes[0],1),
					(7785,"Jupiter", 142981, planet_classes[2],0),
					(14300,"Saturn", 120536, planet_classes[2],0),
					(28800,"Uranus", 51118, planet_classes[0],1),
					(45000,"Neptune", 49500, planet_classes[0],1),
					(59000,"Pluto", 2630, planet_classes[3],1)):
					
		distance = planet[0] # This is sector based, 1 sector is 100,000Km
		name = planet[1]
		planet_diameter = planet[2]
		planet_type = planet[3]
		r = distance * 100000000 # Need actual distance for mapping orbits, this converts it into meters.
		v = math.sqrt((g*mass)/r)
		op = 2*math.pi*math.sqrt(math.pow(r,3)/(g*mass)) 
		iron = planet_diameter*iron_ore[planet_type]
		carbon = planet_diameter*carbon_ore[planet_type]
		oxygen = planet_diameter*oxygen_ore[planet_type]
		h2o = planet_diameter*h2o_ore[planet_type]
		deuterium = planet_diameter*deuterium_ore[planet_type]
		area = (planet_diameter/random.randint(5,10))*planet[4]
		db.universe.insert({'name' : name, 'x_pos' : x+distance, 'y_pos' : y, 'area' : area, 'item' : "planet", 'p_id' : p_id, 'iron' : iron, 'carbon' : carbon, 'oxygen' : oxygen, 'h2o' : h2o, 'deuterium' : deuterium, 'type' : planet_type, 'velocity' : v, 'created' : seconds, 'distance' : distance, 'op' : op})


def create_galaxy():
	# at the center of the galaxy is a black hole... lets start with it. :-)
	name = "Sagittarius A"
	item = "black hole"
	x = 0
	y = 0
	mass = su*4000000
	r = 2*g*mass/math.pow(c,2)
	p_id = db.universe.insert({'name' : name, 'item' : item , 'x_pos' : x, 'y_pos' : y, 'type' : "Super Massive Black Hole", 'diameter' : math.pow(r,2), 'created' : seconds, 'mass' : mass})
	
	# Math for the spiral arms
	track = 0
	e = math.e
	a = r
	static_b = .6 #Controls the spiral 
	deg = 0
	numtails = 5 # number of tails originating from the same point.
	offset = 120/numtails

	for o in range(numtails):

		for s in range(15):
			b = static_b + (0.005*s)  #controls the angle of the spiral arms, 
			# print b
			deg = 0
			while deg < 360:
				
				r = a*math.pow(e,b*math.radians(deg))
				x = r*math.cos(math.radians(deg-(o*offset)))*-1
				y = r*math.sin(math.radians(deg-(o*offset)))*-1
				position = None
				margin = 20*au
				position = db.universe.find_one({"x_pos": {"$gte": x-margin , "$lte": x+margin},"y_pos": {"$gte": y-margin, "$lte": y+margin}})
				deg +=random.uniform(0.0,2)
				if position == None:
				# print int(x)*-1,int(y)*-1


	#The following is a control structure to keep the probability of specific types of stars accurate.
	
					choose_star = random.randrange(1,1000)
					if choose_star <= 750:
						star(6, int(x), int(y), p_id)
					elif choose_star >=751 and choose_star <= 870:
						star(5, int(x), int(y), p_id)
					elif choose_star >=871 and choose_star <= 945:
						star(4, int(x), int(y), p_id)
					elif choose_star >=946 and choose_star <= 975:
						star(3, int(x), int(y), p_id)
					elif choose_star >=976 and choose_star <= 981:
						star(2, int(x), int(y), p_id)
					elif choose_star >= 982 and choose_star <= 983:
						star(1, int(x), int(y), p_id)
					elif choose_star == 984:
						star(0, int(x), int(y), p_id)
					
					
					track +=1
				
			deg = 0
			while deg < 360:
				
				r = a*math.pow(e,b*math.radians(deg))
				x = r*math.cos(math.radians(deg-(o*offset)))
				y = r*math.sin(math.radians(deg-(o*offset)))
				position = None
				margin = 20*au
				position = db.universe.find_one({"x_pos": {"$gte": x-margin , "$lte": x+margin},"y_pos": {"$gte": y-margin, "$lte": y+margin}})
				deg +=random.uniform(0.0,2)
				if position == None:
				# print int(x),int(y)

		
		
	#The following is a control structure to keep the probability of specific types of stars accurate.
	
					choose_star = random.randrange(1,1000)
					if choose_star <= 750:
						star(6, int(x), int(y), p_id)
					elif choose_star >=751 and choose_star <= 870:
						star(5, int(x), int(y), p_id)
					elif choose_star >=871 and choose_star <= 945:
						star(4, int(x), int(y), p_id)
					elif choose_star >=946 and choose_star <= 975:
						star(3, int(x), int(y), p_id)
					elif choose_star >=976 and choose_star <= 981:
						star(2, int(x), int(y), p_id)
					elif choose_star >= 982 and choose_star <= 983:
						star(1, int(x), int(y), p_id)
					elif choose_star == 984:
						star(0, int(x), int(y), p_id)
					
					
					track +=1
								

								
	# Now to fill in the blanks for the galaxy
	
	x_min = db.universe.find().sort("x_pos" , 1).limit(1)
	for a in x_min:
		x_min = a['x_pos']
		
	x_max = db.universe.find().sort("x_pos" , -1).limit(1)
	for a in x_max:
		x_max = a['x_pos']
		
	y_max = db.universe.find().sort("y_pos" , -1).limit(1)
	for a in y_max:
		y_max = a['y_pos']

	y_min = db.universe.find().sort("y_pos" , 1).limit(1)
	for a in y_min:
		y_min = a['y_pos']
	

	d = 0
	for i in range(5000):
		print d
		x = random.randint(x_min,x_max)
		y = random.randint(y_min,y_max)
		margin = 20*au
		position = db.universe.find_one({"x_pos": {"$gte": x-margin , "$lte": x+margin},"y_pos": {"$gte": y-margin, "$lte": y+margin}})
		if position == None:
			choose_star = random.randrange(1,1000)
			if choose_star <= 750:
				star(6, int(x), int(y), p_id)
			elif choose_star >=751 and choose_star <= 870:
				star(5, int(x), int(y), p_id)
			elif choose_star >=871 and choose_star <= 945:
				star(4, int(x), int(y), p_id)
			elif choose_star >=946 and choose_star <= 975:
				star(3, int(x), int(y), p_id)
			elif choose_star >=976 and choose_star <= 981:
				star(2, int(x), int(y), p_id)
			elif choose_star >= 982 and choose_star <= 983:
				star(1, int(x), int(y), p_id)
			elif choose_star == 984:
				star(0, int(x), int(y), p_id)
			d += 1

	print track			
	
	print "D is :",d


	
create_galaxy()				
				
					
					
					
					
					
					
					
					
					
					