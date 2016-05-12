"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db


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
    return redirect("/dashboard/%s" % user.user_id)


@app.route('/logout')
def logout():
    """ Log out. """

    del session["user_id"]
    flash("You have now logged out.")
    return redirect("/")


# @app.route('/register', methods=['GET'])
# def registration_form():
#     """ registration form. """

#     return render_template("registration.html")

# @app.route('/register', methods=['POST'])
# def registration():
#     """ register new user. """

#     """ Get form variables """
#     first_name = request.form["first_name"]
#     last_name = request.form["last_name"]
#     # username = request.form ["username"] --> to be added later
#     email = request.form["email"]
#     password = request.form["password"]
#     age = request.form["age"]

#     new_user = User(first_name=first_name, last_name=last_name, email=email,
#         password=password, age=age)

#     db.session.add(new_user)
#     db.session.commit()

#     flash("User %s %s added." % first_name, last_name)
#     return redirect('/login')


# @app.route('/dashboard/<last_name, int:user_id>') #shows last_name + user_id
# def user_dashboard():
#     """ Interactive Dashboard. """

#     return render_template("dashboard.html")

#     # in dashboard.html, store buttons containing links to new pages 
#     # then route the pages individually 

# @app.route('/dashboard_button')
# def dashboard_button():
#     """ Dashboard button redirect to dashboard. """

#     return render_template("dashboard.html")

# @app.route('/profile/<last_name, int:user_id>')
# def user_profile():
#     """ User profile page. """

#     return render_template("profile.html")

# @app.route('/inbox/<last_name, int:user_id')
# def inbox():
#     """ Messaging inbox. """

#     return render_template("inbox.html")


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
