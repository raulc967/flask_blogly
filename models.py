"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    """Connecting to the database in postgres"""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """ This is a model for the Users that are created by the users """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    image_url = db.Column(db.String(30), nullable=True)
    posts = db.relationship('Posts')

class Posts(db.Model):
    """" This is a model for the Posts that are created by the Users """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User')

class PostTag(db.Model):
    """ This is a model for the tags that are on the posts """
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), primary_key=True)


class Tag(db.Model):
    """ This is a model for the tags """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    posts = db.relationship('Posts', secondary="post_tag", backref="tag")