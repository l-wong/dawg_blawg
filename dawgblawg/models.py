from dawgblawg import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

#from flask_restful import Resource, Api


#load user function used to load current user based on their id to load info specific to user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


#user class inherit from db.Model and UserMixin
class User(db.Model,UserMixin):

    __tablename__= 'users'

    id = db.Column(db.Integer,primary_key=True)
    profile_image = db.Column(db.String(64),default='default_profile.png')
    email = db.Column(db.String(64),unique=True,index=True)
    username = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(250),default='Certified Dog Lover.')

    posts = db.relationship('BlogPost',backref='author',lazy=True)

    def __init__(self,email,username,password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"Username {self.username}"

    def json(self):
        return {'id': self.id,
                'profile_image': self.profile_image,
                'email': self.email,
                'username': self.username,
                'about_me': self.about_me,
                'posts': self.posts}

class BlogPost(db.Model):

    users = db.relationship(User)

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    date = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    title = db.Column(db.String(140),nullable=False)
    text = db.Column(db.Text,nullable=False)

    def __init__(self,title,text,user_id):
        self.title = title
        self.text = text
        self.user_id = user_id

    def __repr__(self):
        return f"Post ID: {self.id} -- Date: {self.date} -- {self.title}"

    def json(self):
        return {'id': self.id,
                'user_id': self.user_id,
                'date': self.date,
                'title': self.title,
                'text': self.Text}

'''
###################REST API########################
class BlawgUsers(Resource):

    def get(self, username):
        usr = User.query.filter_by(username=username).first()
        if usr:
            return usr.json()
        else:
            return {'username': None},404

    def post(self, username):
        pass

    def delete(self,username):
        usr = User.query.filter_by(username=username).first()
        db.session.delete(usr)
        db.session.commit()
        return {'note': 'delete success'}

class AllUsers(Resource):

    def get(self):
        usrs = User.query.all()
        return [usr.json() for usr in usrs]
'''
