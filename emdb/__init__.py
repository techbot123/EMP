from flask import Flask
from emdb.mongo_connector import MongoCon
app = Flask(__name__)
app.config['SECRET_KEY'] = 'sagarisgreat'
mongoclient = MongoCon()
mongoclient = mongoclient.mongo_connector()
from emdb import routes


