"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.User):
    """User information."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    
class Draft(db.Draft):
    """Stores drafts being written by user."""

    __tablename__ = "drafts"

    draft_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    title = db.Column(db.String(200), nullable=True)
    start_date = db.Column(db.DateTime)


    # Define relationship to User

    user = db.relationship("User", backref=db.backref("drafts"))

class Published_Drafts(db.Published):
    """Stores published drafts written by user."""

    __tablename__ = "published"

    publish_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.user_id'))
    draft_id = db.Column(db.Integer, ForeignKey('drafts.draft_id'))
    title = db.Column(db.String(200))
    publish_date = db.Column(db.DateTime)

    # Define relationship to User

    user = db.relationship("User", backref=db.backref('published'))

    # Define relationship to Drafts 

    draft = db.relationship("Drafts", backref=db.backref('published'))








##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ratings'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
