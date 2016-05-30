"""Openbook - A Writing Database"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, flash, redirect, request, jsonify, url_for, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Draft, Published


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "CBA"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """ Homepage with login/register. """
    # import pdb; pdb.set_trace()

    current_session = session.get('user_id', None)
    return render_template("homepage.html")


@app.route('/login', methods=['POST'])
def login():
    """ Processes login. """

    # Get form variables 
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    if not user:
        flash ("User not found. Please register.")
        return redirect("/register")

    if user.password != password:
        flash("Wrong password. Please try again.")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("Welcome {}".format(user.first_name))
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
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    # username = request.form ["username"] --> to be added later
    email = request.form.get("email")
    password = request.form.get("password")
    age = request.form.get("age")

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
def get_drafts_app():
    """ Renders the drafts app """
    return render_template("draft_page.html")


@app.route('/api/drafts', methods=['GET'])
def get_drafts():

    """ 
    Queries and binds to variable 'drafts' before jsonifying for use in 
    drafts.js to pull and display old drafts.

    """
    # collects everything from the Draft class by filtering by user_id in session and
    # saving it in variable, 'drafts'

    drafts = Draft.query.filter_by(user_id=session["user_id"]).all()

    # for draft in drafts (the collection from above), run function to.dict() on draft
    # to store each draft in dictionary form in a list.

    draft_dicts = [draft.to_dict() for draft in drafts]

    # jsonify key 'drafts' with the value draft_dicts - a list of dictionaries of each draft,
    # of all the drafts 
    
    return jsonify({'drafts': draft_dicts})

@app.route('/new_draft', methods=['GET'])
def set_new_draft():

    """ Renders the template for the new_draft.html page. """

    return render_template('new_draft.html')

@app.route('/new_draft.json', methods=['POST'])
def new_draft():

    """ Grabs what is posted in new_draft and commits to DB. """

    title = request.form.get("title-field") #grabs title from the new draft 
    draft = request.form.get("draft-field") #grabs draft from the new draft
    user_id = session["user_id"]
    user = User.query.filter(User.user_id == user_id).one()

    new_draft = Draft(title=title, draft=draft, user_id=user_id)

    # once it stores in db, will be converted into a dictionary through 
    # to_dict method

    db.session.add(new_draft)
    db.session.commit()

    # session['draft_id'] = new_draft.draft_id 
    # would you want to have the draft id in session?

    return redirect("/draft_page")


@app.route('/save_draft', methods=['POST'])
def save_draft():
    """ Saves new draft to template 'draft' so draft_id is saved only once. """

    # import pdb; pdb.set_trace()

    # here is the real request for an object
    #form is for a post request

    #reassigning variable names to dict values from save_draft.js

    new_title = request.form.get("title") #contains value id title_field
    new_draft = request.form.get("draft") #contains value id draft_field
    new_id = request.form.get("id")
    user_id = session["user_id"]

    print new_draft
    print new_title

    # import pdb; pdb.set_trace()

    # if this draft_id is in session
    # query by that draft_id to get the attributes stored in the object
    draft = Draft.query.filter(Draft.draft_id == int(new_id)).one()
   
    
    # reassign new variables from above, containing the values of dict formInputs
    draft.draft = new_draft
    draft.title = new_title

    db.session.add(draft)
    db.session.commit()

    return jsonify({'draft_id': draft.draft_id, 'draft_title': draft.title})

    # else: 
    # Draft is the class; everything in () are attributes
    # binding the object to var saving_draft
    # makes saving_draft the object 
    # else:
    #     saving_draft = Draft(title=new_title, draft=new_draft, user_id=user_id)

    #     db.session.add(saving_draft)
    #     db.session.commit()

    #     # saved_draft = Draft.query.filter_by(title=title, draft=draft, user_id=user_id).first()
    #     session['draft_id'] = saving_draft.draft_id

    #     return jsonify({'draft_id': saving_draft.draft_id, 'draft_title': saving_draft.title})

    #do I need to jsonify anything to keep the writing on the page or should I have this reload?
    #should I save this as a dictionary in python to be JSON-ified into an object for editing?

@app.route('/draft_page/<int:draft_id>')
def get_one_draft(draft_id):

    """ 
    On click will grab a specific draft from the leftside list and present it in 
    the editor on the right side of the page.

    """

    draft = Draft.query.get(draft_id)

    return render_template("draft_page.html", draft=draft)

    #on 'click' retrieve a single draft and display it on the rightside of the screen
    #for edit or review 

@app.route('/publish_draft', methods=['POST'])
def publish_new_draft():

    title = request.form.get("title")
    draft = request.form.get("draft")
    user_id = session["user_id"]
    draft_id = session["draft_id"]

    publish_draft = Published(title=title, draft=draft, user_id=user_id)

    saved = Draft.query.filter_by(draft_id=draft_id).first()

    db.session.add(publish_draft)
    db.session.commit()

    publishing = Published.query.filter_by(title=title, draft=draft, user_id=user_id, draft_id=draft_id)
    session['publish_id'] = publishing.publish_id

    publish = Published.query.filter_by(user_id=session["user_id"]).first()

    return redirect("/dashboard", publish=publish)


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
