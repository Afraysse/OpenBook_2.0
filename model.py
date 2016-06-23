"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy

import datetime

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

class User(db.Model):
    """User information."""

    __tablename__ = "user"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    # Put name inside TSVectorType definition for it to be fulltext-indexed (searchable)
    search_vector = db.Column(TSVectorType('first_name', 'last_name'))


    # draft_count = db.Column(db.Integer, nullable = True)
    # publish_count = db.Column(db.Integer, nullable = True)

    def __repr__(self):

        return "<User user_id={} email={}>".format(self.user_id, self.email)

    def to_dict(self):
        return {
            'id': self.user_id,
            'name': '%s %s' % (self.first_name, self.last_name),
            'email': self.email,
            'age': self.age
        }
    
class Draft(db.Model):
    """Stores drafts being written by user."""

    __tablename__ = "drafts"

    draft_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    draft = db.Column(db.String(10000), nullable=False)
    title = db.Column(db.String(200), nullable=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

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
    draft_id = db.Column(db.Integer, db.ForeignKey('drafts.draft_id'))
    title = db.Column(db.String(200), nullable=False)
    draft = db.Column(db.String(10000), nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    # # Define relationship to User
    user = db.relationship("User", backref=db.backref("published", order_by=user_id))

    # Define relationship to Books 
    drafts = db.relationship("Draft", backref=db.backref("published", order_by=draft_id))


    def __repr__(self):

        return "<Published publish_id={} title={} user_id={} date={}>".format(self.publish_id, 
                                                                            self.title, 
                                                                            self.user_id, 
                                                                            self.date)
    def to_dict(self):
        return {
            'id': self.publish_id,
            'user': self.user.to_dict(),
            'draft': self.drafts.to_dict(),
            'title': self.title,
            'draft': self.draft
            # 'date': self.date
        }

class Relations(db.Model):
    "Connect two users to establish a friendship and allow for info viewing"

    __tablename__ = "relationships"

    relationship_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_a_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    user_b_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    status = db.Column(db.String(100), nullable=False)

    # Define relationships between users
    user_a_id = db.relationship("User", backref=db.backref("user"))
    user_b_id = db.relationship("User", backref=db.backref("user"))

    def __repr__(self):
        """Provide helpful representation when printed"""

        return "<Relations relationship_id=%s user_a_id=%s user_b_id=%s status=%s>" % (self.relationship_id,
                                                                                        self.user_a_id,
                                                                                        self.user_b_id,
                                                                                        self.status)

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
