# db_config.py
import pymysql
pymysql.install_as_MySQLdb()  # Make PyMySQL act as MySQLdb

from flask import Flask
from flaskext.mysql import MySQL  # flask-mysql, not flask-mysqldb

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'evahub'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

# Initialize MySQL
mysql = MySQL()
mysql.init_app(app)  # Note: flask-mysql uses init_app

# Function to get a connection (cursor-ready)
def getDb():
    connection = mysql.connect()
    return connection

def fromDbConfig():
    print("yeah from the db_config")
