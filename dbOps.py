import time
import datetime
import uuid


from datetime import datetime
from time import strftime
from db import db



def ts(add=0):
	"""	Gets the current time and formats it into a human readable string
	"""
	st = datetime.fromtimestamp(time.time()+add).strftime('%m-%d-%Y %H:%M:%S')
	return st

	
def log(mongoDb, col, type, query, module, user, lvl = "INFO", error = ""):
	""" Logs the action performed on the database with the user specified.
	"""
	logEntry = {
		'lvl' : lvl, 
		'db' : mongoDb,
		'collection' : col,
		'type' : type,
		'query' : str(query), 
		'user' : user,
		'modlue' : module,
		'timeStamp' : ts(),
		'whenCreated' : time.time(),
		'whenChanged' : time.time(),
		'error' : error
	}
	db('local')['mongo'].insert( logEntry )

	
def timeline( timeline, title, comment, user="CONSOLE" ):
	print "timeline Called"
	newtime = {
		'date' : ts()[:10],
		'title' : title,
		'comment' : comment,
		'user' : user,
		'whenCreated' : time.time(),
		'whenChanged' : time.time(),
	}
	timeline.append(newtime)
	return timeline
		

	
class MongoOps:
	""" QUERY FUNCTIONS """

	def queryOne( self, database, collection, query, user="CONSOLE" ):
		"""	Queries the specifed database, collection and returns the object found. 
			If nothing is found, None will be returned
		"""
		try:
			log( database, collection, "query", query, "dbOps.MongoOps.queryOne", user )
			return db(database)[collection].find_one(query)
		except Exception as err:
			print "ERROR with queryOne", err
			return None
		
	def queryAll( self, database, collection, query, user="CONSOLE" ):
		"""	Queries the specifed database, collection and returns the objects found. 
			If nothing is found, None will be returned
		"""
		try:
			log( database, collection, "query", query, "dbOps.MongoOps.queryAll", user )
			return db(database)[collection].find(query)
		except Exception as err:
			print err
			return None
			
	def queryOneField( self, database, collection, query, field, user="CONSOLE"):
		""" Queries one object and returns the specified field.
			If nothing is found, returns an empty string.
		"""
		try:
			log( database, collection, "query", query, "dbOps.MongoOps.queryOneField", user )
			return db(database)[collection].find_one(query)[field]
		except Exception as err:
			print err
			return ""

			

	""" UPDATE FUNCTIONS """	
	def updateOne( self, database, collection, query, edit, user="CONSOLE", upsert=True):
		""" Updates a single document based on the query
			If the query doesn't match any documents. It will insert a document with the information provided
			returns the result
		"""
		try:
			edit.update( {'whenChanged' : time.time(), 'lastUpdateBy' : user, 'lastUpdateTs' : ts()} )
			log( database, collection, "update", query, "dbOps.MongoOps.updateOne", user )
			return db(database)[collection].update_one(query, {'$set' : edit}, upsert)
		except Exception as err:
			print err
			return None
		
	def updateAll( self, database, collection, query, edit, user="CONSOLE" ):
		""" Updates all documents based on the query
			If the query doesn't match any documents. It will insert a document with the information provided
			returns the result
		"""
		try:
			edit.update( {'whenChanged' : time.time(), 'lastUpdateBy' : user, 'lastUpdateTs' : ts()} )
			log( database, collection, "update", query, user, "dbOps.MongoOps.updateAll", user )
			return db(database)[collection].update_many( query, {'$set' : edit} )
		except Exception as err:
			print err
			return None
			
	""" DELETE FUNCTIONS """
	
	def deleteOne( self, database, collection, query, user="CONSOLE", backup=False):
		""" Deletes a single document based on the query
			IF backup is set to true, it will put a copy of the deleted object into the restores collection.
		"""
		try:
			edit = self.queryOne( database, collection, query, user )
			edit.update( {'whenChanged' : time.time(), 'lastUpdateBy' : user, 'lastUpdateTs' : ts()} )
			log( database, collection, "delete", query, user, "dbOps.MongoOps.deleteOne" )
			if backup:
				self.updateOne( database, collection+"_deleted", query, edit, user )
			return db(database)[collection].delete_one( query )
		except Exception as err:
			print err
			return None
	
	def deleteAll( self, daatabase, collection, query, user="ONSOLE", backup=False):
		""" Deletes all documents based on a query
			If backup is set to true, it will put a copy of the deleted objects into the restores collection
		"""
		try:
			objs = self.queryAll( database, collection, query )
			for obj in objs:
				deleteOne( database, collection, {'_id' : obj['_id']} )
		except Exception as err:
			print err
			return None