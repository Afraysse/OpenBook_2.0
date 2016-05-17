"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, flash, redirect, session, request
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Book, Published


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """ Homepage with login/register. """

    return render_template("homepage.html")


@app.route('/login', methods=['GET'])
def login_form():
    """Login form."""

    return render_template("login.html")

    #form variables for route: email and password

@app.route('/login', methods=['POST'])
def login():
    """ Processes login. """

    # Get form variables 
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash ("User not found. Please register.")
        return redirect("/register")

    if user.password != password:
        flash("Wrong password. Please try again.")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("Welcome!")
    return redirect("/dashboard")


@app.route('/logout')
def logout():
    """ Log out. """

    del session["user_id"]
    flash("You have now logged out.")
    return redirect("/")


@app.route('/register', methods=['GET'])
def registration_form():
    """ registration form. """

    return render_template("registration.html")

@app.route('/register', methods=['POST'])
def registration():
    """ register new user. """

    """ Get form variables """
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    # username = request.form ["username"] --> to be added later
    email = request.form["email"]
    password = request.form["password"]
    age = request.form["age"]

    new_user = User(first_name=first_name, last_name=last_name, email=email,
        password=password, age=age)

    db.session.add(new_user)
    db.session.commit()

    flash("User {} {} added.".format(first_name, last_name))
    return redirect('/login')


@app.route('/dashboard') #shows last_name + user_id
def user_dashboard():
    """ Interactive Dashboard. """

    #publish post = Published.query.all()

    #jinja: if published_posts: for --> iterate over

    #working on adding functions to dashboard and profile

    #add a high testing percentage


    return render_template("dashboard.html")

# @app.route('/profile')
# def user_profile():
#     """ User profile page. """

#     return render_template("profile.html")

# @app.route('/inbox')
# def user_messaging():
#     """ Messaging Inbox. """

#     return render_template("inbox.html")

# @app.route('/explore')
# def user_explore():
#     """ Explore the unfollowed. """

#     return render_template("explore.html")

@app.route('/working_draft', methods=['GET'])
def working_draft():
    """ User writes down something new. """

    return render_template("new_draft.html")

@app.route('/working_draft', methods=['POST'])
def submit_draft():
    """ Saves user's draft to data. """

    title = request.form["title"]
    draft = request.form["new-draft"] 
    user_id = session["user_id"]

    book_draft = Book(title=title, draft=draft, user_id=user_id)
    

    db.session.add(book_draft)
    db.session.commit()

    book = Book.query.filter_by(title=title, draft=draft, user_id=user_id)
    session['book_id'] = book.book_id

    return redirect('/profile')

@app.route('/publish_book/publish', methods=['POST'])
def publish_draft():

    title = request.form["title"]
    draft = request.form["new-draft"]
    user_id = session["user_id"]


    published_draft = Published(title=title, draft=draft, user_id=user_id)

    db.session.add(published_draft)
    db.session.commit()

    return jsonify({'publish': 'success'})


# @app.route('/publish', methods=['GET'])
# def get_publish():
#     """ Routes draft to be published. """

#     return render_template('published.html')

# @app.route('/publish', methods=['POST'])
#     """ Posts draft to be published. """

#     user.

#     return redirect('/dashboard')










##############################################################################
# Connects to DB

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
