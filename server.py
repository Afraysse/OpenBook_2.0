"""Openbook - A Writing Database"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, flash, redirect, session, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Draft, Published


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """ Homepage with login/register. """
    # import pdb; pdb.set_trace()

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
    return redirect('/feed')


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


@app.route('/feed') #feed
def user_dashboard():
    """ Interactive feed. """

    return render_template("feed.html")


@app.route('/profile/<int:user_id>')
def user_detail(user_id):
    """ Show info about user. """

    # Button will take you to book list 

    user = User.query.get(user_id)
    return render_template("profile.html", user=user)

################################################################################

# Routes for draft_page.html - basically all draft functions

@app.route('/draft_page')
def render_new_draft_template():
    """ Renders new_draft template """


    return render_template("draft_page.html")


@app.route('/get_drafts', methods=['GET'])
def get_old_drafts():

    """ 
    Pulls all drafts stored in database and presents them in the 
    HTML file new_draft, ordered_by draft_id. 

    """
    import pdb; pdb.set_trace()

    drafts = Draft.query.filter_by(user_id=session["user_id"]).all()

    draft_list = []

    if drafts:
        for draft in drafts:
            draft_dict = {
                "draft_id": draft.draft_id,
                "user_id": draft.user_id,
                "title": draft.title,
                "draft": draft.draft
        }

            draft_list.append(draft_dict)

    return jsonify({"draft_list": draft_list})

@app.route('/draft/<int:draft_id>', methods=['GET'])
def get_one_draft():

    """ 
    On click will grab a specific draft from the leftside list and present it in 
    the editor on the right side of the page.

    """

    draft = Draft.query.get(draft_id)

    one_draft = {
        "title": title,
        "draft": draft,
        }

    return jsonify(one_draft)

    #on 'click' retrieve a single draft and display it on the rightside of the screen
    #for edit or review 

@app.route('/overwrite_draft', methods=['POST'])
def overwrite():

    return jsonify({'success': 'true'})

# when you hit save, this overwrites the previous copy, perserving the draft_id to 
# one draft_id per draft stored in Draft db


@app.route('/save_draft', methods=['POST'])
def save_draft():
    """ Saves new draft to template 'draft' so draft_id is saved only once. """

    title = request.form["title"]
    draft = request.form["draft"]
    user_id = session["user_id"]

    # if session[]


    # else: 
    saving_draft = Draft(title=title, draft=draft, user_id=user_id)

    db.session.add(saving_draft)
    db.session.commit()

    draft = Draft.query.filter_by(title=title, draft=draft, user_id=user_id).first()
    session['draft_id'] = draft.draft_id

    return "Successfully Saved!"

    #do I need to jsonify anything to keep the writing on the page or should I have this reload?
    #should I save this as a dictionary in python to be JSON-ified into an object for editing?


@app.route('/drafts/<int:draft_id>', methods=['DEL'])
def delete_draft(draft_id):

    """ Deletes current draft, whether saved or new. """

    #need to add in data 

@app.route('/publish_draft', methods=['POST'])
def publish_new_draft():

    title = request.form["title"]
    draft = request.form["draft"]
    user_id = request.form["user_id"]
    draft_id = request.form["draft_id"]

    publish_draft = Published(title=title, draft=draft, user_id=user_id, draft_id=draft_id)

    saved = Draft.query.filter_by(draft_id=draft_id).first()

    db.session.add(publish_draft)
    db.session.commit()

    publishing = Published.query.filter_by(title=title, draft=draft, user_id=user_id, draft_id=draft_id)
    session['publish_id'] = publishing.publish_id

    return redirect("/dashboard", draft_id=draft_id)


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
