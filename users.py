## -*- coding: utf-8 -*-
import web
import json
import time

import ships


from dbOps import MongoOps
from sessionOps import SessionMgr

def getUser():
	try:
		return MongoOps().queryOne( 'remote', 'users', {'id' : web.cookies().get('id')} )
		# return json.loads(web.cookies().get('profile'))
	except Exception as err:
		print err
		

def login_required(function, login_page='/'):
	def inner(*args, **kwargs):
		if SessionMgr().getSession():
			return function(*args, **kwargs)
		else:
			print "No session found"
			raise web.seeother("/landing")
	return inner

def newUser(obj):
	print "newUser Called"
	try:
		profile = MongoOps().queryOne( 'local', 'tempProfiles', {'id' : web.cookies().get('id')} )
		MongoOps().updateOne( 'remote', 'ships', {}, ships.gcbs_371(profile['id'], profile['id']), upsert=True )
		battleship = MongoOps().queryOne( 'remote', 'ships', {'ownerId' : profile['id'], 'class' : "BattleShip"} )
		u = {
				'id' : profile['id'],
				'rank' : {
					'lvl' : 3,
					'experience' : 1000,
					'title' : "Captian",
				},
				'cDetails' : {
					'cGender' : "",
					'cName' : obj['characterName'],
					'cRace' : obj['characterRace'],
				},
				'gProfile' : profile,
				'suspended' : False,
				'verified' : True,
				'ships' : [battleship['_id']],
				'piloting' : battleship['_id'],
			}
		MongoOps().updateOne( 'remote', 'users', {'id' : profile['id']}, u )
		MongoOps().deleteOne( 'local', 'tempProfiles', {'id' : profile['id']} )
		web.setcookie('id', "", -1)
		print "completed new user"
		raise web.seeother("/")
	except Exception as err:
		print err
		return err