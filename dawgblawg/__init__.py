import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager
#from flask_restful import Resource, Api

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

### DATABASE SETUP ###
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#create db
db = SQLAlchemy(app)
Migrate(app,db) #to form migrations
#manager = Manager(app)
#manager.add_command('db', MigrateCommand)

#from dawgblawg.models import BlawgUsers, AllUsers

#api = Api(app)
#jwt = JWT(app,authenticate,identity)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"

#register blueprints
from dawgblawg.core.views import core
from dawgblawg.users.views import users
from dawgblawg.error_pages.handlers import error_pages
from dawgblawg.blog_posts.views import blog_posts

app.register_blueprint(core)
app.register_blueprint(error_pages)
app.register_blueprint(users)
app.register_blueprint(blog_posts)

#api.add_resource(BlawgUsers,'/user/<string:username>')
#api.add_resource(AllUsers,'/users')
