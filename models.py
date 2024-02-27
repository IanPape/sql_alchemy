from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer

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
