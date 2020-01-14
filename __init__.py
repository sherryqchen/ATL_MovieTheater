from flask import Flask
from flask_mysqldb import MySQL
from flask_login import LoginManager
import yaml


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

# Enter your database connection details below
db = yaml.load(open('app/static/db.yaml'))
app.config['MYSQL_HOST'] = db['MYSQL_HOST']
app.config['MYSQL_USER'] = db['MYSQL_USER']
app.config['MYSQL_PASSWORD'] = db['MYSQL_PASSWORD']
app.config['MYSQL_DB'] = db['MYSQL_DB']

# Intialize MySQL
mysql = MySQL(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'


from app import main
