from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

"""Models for Blogly."""

class User(db.Model):
    __tablename__ = 'users'

    id= db.Column(Integer,
                  primary_key= True,
                  autoincrement=True)
    first_name=db.Column(db.String(20))
    last_name=db.Column(db.String(50))
    image_url=db.Column(db.String)

class Post(db.Model):
    __tablename__='post'

    id=db.Column(Integer, 
                 primary_key=True,
                 autoincrement=True)
    title=db.Column(db.String(50))
    content=db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=db.func.now(), server_default=db.func.now())
    user_id= db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user= relationship('User', backref=db.backref('posts', lazy='dynamic'))
    
