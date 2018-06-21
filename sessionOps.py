import time
import web
import uuid

from dbOps import MongoOps, ts



class SessionMgr(MongoOps):

	def newSession(self, id, ip):
		try:
			s = {
			'id' : id,
			'whenCreated' : time.time(),
			'whenChanged' : time.time(),
			'whenExpires' : time.time()+3600, #1 hour
			'ip' : ip,
			}
			self.updateOne( 'local', 'sessions', {'id' : id, 'ip' : ip}, s )
			web.setcookie( 'id' , s['id'] )
		except Exception as err:
			print "ERR with newSession: ", err
			
	def getSession(self):
		try:
			if self.queryOne( 'local', 'sessions', {'id' : web.cookies().get('id')} ):
				print self.updateOne( 'local' , 'sessions', {'id' : web.cookies().get('id')}, {'whenExpires' : time.time()+3600}, upsert=False)
				return True
		except Exception as err:
			print "ERR with getSession: ", err
			return False

	def killSession(self):
		try:
			MongoOps().deleteOne( 'local', 'sessions', {'id' : web.cookies().get('id')} )
			web.setcookie( 'id' , "", -1 )
		except Exception as err:
			print "ERR with killSession: ", err
			
			