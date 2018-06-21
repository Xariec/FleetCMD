#!/usr/bin/env python
# -*- coding:utf-8 -*-

import web
import urllib
import urlparse
import json

from dbOps import MongoOps, ts
from sessionOps import SessionMgr


class handler(MongoOps):
	"""Authentication and authorization of users by OAuth 2.0
	""" 
	def on_signin(self, profile):
		""" When the user is signing in, this sets up the session.
		If they are already signed in based on a cookie, then just direct them to index
		else, re-generate the session. sends the id to the browser so it can be called later.
		"""
		# web.setcookie('tempProfle', profile, 'Expires', -1)
		# web.setcookie('profile', profile)
		print "on_signin"
		try:
			u = self.queryOne( 'remote', 'users', {'id' : profile['id']} )
			print "found u"
			if u['suspended']:
				raise web.seeother('/suspended')
			if u['verified']:
				if SessionMgr().newSession( profile['id'], web.ctx.get('ip')):
					raise web.seeother('index.html')
		except Exception as err:
			print "Error in on_signin: ", err
			# the error is no user exists, create registration page and direct them to that here.
			self.updateOne( 'local', 'tempProfiles', {'id' : profile['id']}, profile, upsert=True )
			web.setcookie('id', profile['id'])
			raise web.seeother('/register')
		raise web.seeother('/')

	def _http_get(self, url, args=None):
		"""Python HTTP GET request
		url: fullpath, e.g., https://example.org/home
		args (optional): dict used to build query string, e.g.,
		{a: '1', b: '2'} => a=1&b=2
		"""
		if args == None:
			response = urllib.urlopen(url)
		else:
			query_string = urllib.urlencode(args)
			response = urllib.urlopen('%s?%s' % (url, query_string))
			return response

	def _http_post(self, url, args):
		"""Python HTTP POST request
		url: fullpath, e.g., https://example.org/home
		args (optional): dict used to build POST data, e.g.,
		  {a: '1', b: '2'} => a=1&b=2
		"""
		data = urllib.urlencode(args)
		response = urllib.urlopen(url, data)
		return response

	def _oauth2_init(self):
		"""Step 1 of oauth 2.0: init the oauth 2.0 login flow for web
		Send users to login page of provider (like Google or Facebook) for
		authentication and ask authorization of user data.
		"""
		args = {
			'response_type': 'code',
			'client_id': '672734064270-s8ie5n74plsnq4s9bi5d92jieofe7e29.apps.googleusercontent.com', 
			'redirect_uri': 'http://www.xariec.com/auth/google/callback',
			'scope': 'https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email'
		}
		raise web.seeother('https://accounts.google.com/o/oauth2/auth' + '?' + urllib.urlencode(args))

	def _oauth2_callback(self):
		"""Step 2 of oauth 2.0: Handling response from login page of providers.
		Case 1) If auth (authentication and authorization) not ok, raise Exception.
		Case 2) If auth ok, get access_token first, and then use the access_token to
		retrieve user profile.
		"""

		# check whether auth is ok, if not ok, raise Exception.
		error = web.input().get('error')
		if error:
			print error
			raise Exception(error)
		# auth ok, get access_token
		args = {
		'code': web.input().get('code'),
		'client_id': '672734064270-s8ie5n74plsnq4s9bi5d92jieofe7e29.apps.googleusercontent.com', 
		'client_secret': '7mgCz9eMcrh7EsMXImZapfDn', 
		'redirect_uri': 'http://www.xariec.com/auth/google/callback',
		'grant_type': 'authorization_code'
		}

		_parser = getattr(self, '_json_parser')
		response = _parser(
		self._http_post('https://accounts.google.com/o/oauth2/token', args).read() )
		if response.get('error'):
			raise Exception(response)

		# access_token is ready, get user profile.
		_fetcher = getattr(self, '_get_google_user_data')
		profile = _fetcher(response['access_token'])

		# user profile ok. call on_signin function
		self.on_signin(profile)

	def _get_google_user_data(self, access_token):
		"""Obtaining User Profile Information from Google API
		userinfo endpoint:
		https://www.googleapis.com/oauth2/v3/userinfo
		"""
		profile = json.loads(
			self._http_get('https://www.googleapis.com/oauth2/v3/userinfo',
						   dict(access_token=access_token)).read()
			)
		if 'id' not in profile and 'sub' in profile:
			profile['id'] = profile['sub']		
		return profile

	def _json_parser(self, string):
		"""Parse JSON format string, and return Python dict object
		"""
		return json.loads(string)
		
