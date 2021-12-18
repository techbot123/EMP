from flask import Flask
from emdb.mongo_connector import MongoCon

#Initialize Flask App
app = Flask(__name__)
app.config['SECRET_KEY'] = 'sagarisgreat'
#Initialize MongoDB
mongoclient = MongoCon()
mongoclient = mongoclient.mongo_connector()
db = mongoclient['Employee']
from flask_login import LoginManager
# Initialize Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from emdb import routes

from emdb.employee.routes import employee_b
from emdb.owner.routes import owner_b

app.register_blueprint(employee_b, url_prefix = '/employees')
app.register_blueprint(owner_b, url_prefix = '/owners')
