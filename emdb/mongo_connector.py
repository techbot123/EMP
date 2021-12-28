import pymongo
from pymongo import MongoClient
import urllib
from getpass import getpass

class MongoCon:
	def get_mongo_client(self, username, pwd):
		self.client = MongoClient('mongodb+srv://{}:{}@cluster0.n1b6n.mongodb.net/Employee?retryWrites=true&w=majority'.format(username, urllib.parse.quote_plus(pwd)))
		try:
			self.client.list_database_names()
		except Exception as e:
			print(e)
		else:
			return self.client

	def mongo_connector(self):
		# username = input('Enter Username for Mongo DB: ')
		username = 'techsy'
		# pwd = getpass(prompt = 'Enter Password: ')
		pwd = 'hehe'
		# print(username, pwd)
		return self.get_mongo_client(username, pwd)
