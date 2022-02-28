from flask import Flask
from flask_admin import Admin
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os, secrets


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'vartotojai.db?check_same_thread=False')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True



db = SQLAlchemy(app)
Migrate(app, db)

admin = Admin(app)
login_manager = LoginManager(app)
login_manager.login_message_category = 'info'
login_manager.login_view = 'registracija'





from autoservisas import routes