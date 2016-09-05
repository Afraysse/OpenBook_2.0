"""Models and database functions for Ratings project."""
from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from markdown import markdown 
import bleach
from flask import current_app, request, url_for
from flask_login import UserMixin, AnonymousUserMixin
from flask_sqlalchemy import SQLAlchemy


# SQLAlchemy-searchable is the library used for search engines 

from sqlalchemy_searchable import make_searchable
from sqlalchemy_utils.types import TSVectorType
# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()

make_searchable()


##############################################################################
# Model definitions

class Relations(db.Model):
    """ Contains Follower/Followed information. """
    __tablename__ = 'relations'

    follower_id = db.Column(db.Integer, db.ForeignKey('user.user_id'),
                            primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.user_id'),
                            primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class User(UserMixin, db.Model):
    """ Contains user information. """

    __tablename__ = "user"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String, nullable=False)
    confirmed = db.Column(db.Boolean, default=False)
    location = db.Column(db.String(80), nullable=False)
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    # avatar_hash = db.Column(db.String(32))
    age = db.Column(db.Integer, nullable=True)
    password = db.Column(db.String(128), nullable=False)
    followed = db.relationship('Relations',
                                foreign_keys=[Relations.follower_id],
                                backref=db.backref('follower', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')
    followers = db.relationship('Relations',
                                foreign_keys=[Relations.followed_id],
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')

    # Put name inside TSVectorType definition for it to be fulltext-indexed (searchable)
    search_vector = db.Column(TSVectorType('first_name', 'last_name'))

    def __repr__(self):

        return "<User user_id={} email={}>".format(self.user_id, self.email)


    # @property 
    # def password(self, password):
    #     self.password_hash = generate_password_hash(password)

    # def verify_password(self, password):
    #     return check_password_hash(self.password_hash, password)

# class User(db.Model):
#     """User information."""

#     __tablename__ = "user"

#     user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     first_name = db.Column(db.String(100), nullable=False)
#     last_name = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(64), nullable=False)
#     password = db.Column(db.String(64), nullable=False)
#     age = db.Column(db.Integer, nullable=False)

#     # Put name inside TSVectorType definition for it to be fulltext-indexed (searchable)
#     search_vector = db.Column(TSVectorType('first_name', 'last_name'))


#     # draft_count = db.Column(db.Integer, nullable = True)
#     # publish_count = db.Column(db.Integer, nullable = True)

#     def __repr__(self):

#         return "<User user_id={} email={}>".format(self.user_id, self.email)

#     def to_dict(self):
#         return {
#             'id': self.user_id,
#             'name': '%s %s' % (self.first_name, self.last_name),
#             'email': self.email,
#             'age': self.age
#         }
    
class Draft(db.Model):
    """Stores drafts being written by user."""

    __tablename__ = "drafts"

    draft_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    draft = db.Column(db.String(10000), nullable=False)
    title = db.Column(db.String(200), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    # Define relationship to User
    user = db.relationship("User", backref=db.backref("drafts", order_by=user_id))


    def __repr__(self):

        return "<Draft draft_id={} draft={} title={}>".format(self.draft_id, self.draft, self.title)

    def to_dict(self):
        return {
            'id': self.draft_id,
            'user': self.user.to_dict(),
            'contents': self.draft,
            'title': self.title,
            'date': self.date,
        }


class Published(db.Model):
    """Stores published drafts written by user."""

    __tablename__ = "published"

    publish_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    draft_id = db.Column(db.Integer, db.ForeignKey('drafts.draft_id'), nullable=True)
    title = db.Column(db.String(200), nullable=False)
    draft = db.Column(db.String(10000), nullable=False)
    # date = db.Column(db.DateTime, default=datetime.utcnow)
    comments = db.relationship('Comment', backref='published', lazy='dynamic')

    # # Define relationship to User
    user = db.relationship("User", backref=db.backref("published", order_by=user_id))

    # Define relationship to Drafts
    drafts = db.relationship("Draft", backref=db.backref("published", order_by=draft_id))


    def __repr__(self):

        return "<Published publish_id={} title={} user_id={}>".format(self.publish_id, 
                                                                            self.title, 
                                                                            self.user_id)
    def to_dict(self):
        return {
            'id': self.publish_id,
            'user': self.user.to_dict(),
            'draft': self.drafts.to_dict(),
            'title': self.title,
            'draft': self.draft,
            # 'date': self.date,
        }

class Comment(db.Model):
    """ save User's comments."""

    __tablename__ = 'comments'

    comment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    post_id = db.Column(db.Integer, db.ForeignKey('published.publish_id'))

##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///openbook'
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
