from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
# Database Path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# secret key to display Flask Forms
app.config['SECRET_KEY'] = '982cb978c1a6e204ad3fb8a0'
# database init
db = SQLAlchemy(app, session_options={"autoflush": False})
# password hash mechanism
bcrypt = Bcrypt(app)
# flask login management
login_manager = LoginManager(app)
# redirect for users not yet logged in
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'info'

from store import routes
from store import models
