from flask import Flask, request, jsonify, render_template, redirect
from flask_sqlalchemy import SQLAlchemy ## for the databaset
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db?timeout=30'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db?timeout=20'

app.config['SECRET_KEY'] = 'c85637535d7d7f6789070d82'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# # Increase the timeout
# app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
#     'connect_args': {'timeout': 15}
# }

db= SQLAlchemy(app=app) ## pass the app as an arg to the db
bcrypt = Bcrypt(app=app)
login_manager = LoginManager(app=app)
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'info'
from market import routes 

# from sqlalchemy import create_engine
# engine = create_engine('sqlite:///your_database.db', connect_args={'check_same_thread': False})
