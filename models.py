from flask_login import UserMixin
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# from sqlalchemy.dialects.postgresql.base import PGDialect

# def _get_server_version_info(self, connection):
#         return (10,0,0) # specify the version of pg redshift emulates. this is just an example

# PGDialect._get_server_version_info = _get_server_version_info

db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://Samuel:5mMdN8QLVMJbtSbRJ-Fz_g@a3b53f4b4941845589eca7636da74b11-bae2dbe13feb05e0.elb.eu-central-1.amazonaws.com:26257/defaultdb?sslmode=verify-ca&options=-c+cockroachdb+version+%2722.2.7%27'
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'connect_args': {
        'sslmode': 'require',
        'options': '--cluster=5mMdN8QLVMJbtSbRJ-Fz_g'
    }
}
db = SQLAlchemy(app)

post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable = False)
    messages = db.relationship('Message', backref='author')
    posts = db.relationship('Post', backref='author')
    profile_image = db.Column(db.String(20), nullable=False, default='default.jpg')
    is_counselor = db.Column(db.Boolean, default=False)

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_sent = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy=True)
    tags = db.relationship('Tag', secondary=post_tags, lazy='subquery',
        backref=db.backref('posts', lazy=True))

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

with app.app_context():
  db.create_all()

