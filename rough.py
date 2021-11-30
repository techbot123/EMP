# import posts as ps
# from getpass import getpass
# # username = input('Enter username')
# passw = getpass(prompt = 'Enter Pass')
# print(passw)
from emdb.mongo_connector import MongoCon

client = MongoCon()

client.mongo_connector()