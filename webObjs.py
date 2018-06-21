import web

from dbOps import MongoOps


class Objs(MongoOps):

	def _getObj(self, request):
		""" Helper function for getting specific objects from the db. 
		This will return the entire object.
		"""
		try:
			if request['value'] == "id":
				request.update( { 'value' : web.cookies().get('id')} )
			return self.queryOne( 'remote', request['col'], {request['key'] : request['value']} )
		except Exception as err:
			print err
			return {}
			